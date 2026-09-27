"""Check that the pipeline modelled every order the generator loaded.

Meant to be piped into a container that has duckdb and the warehouse mounted:

    docker compose exec -T -e EXPECTED_ORDERS=<n> superset python - < this

fct_orders holds one row per order in the OLTP database, so the count the
caller reads out of Postgres is the number to expect here. Deriving it that way
rather than hardcoding the generator's defaults keeps the check honest if those
defaults change.
"""

import os
import sys
import time

import duckdb

WAREHOUSE = os.environ.get("WAREHOUSE_PATH", "/app/superset_home/db/datamart.duckdb")
TIMEOUT = int(os.environ.get("CHECK_TIMEOUT_SECONDS", "900"))

want = int(os.environ["EXPECTED_ORDERS"])
if want <= 0:
    sys.exit("::error::the generator loaded no orders; nothing to model")


def fct_rows():
    """Row count of fct_orders, or None while it is not readable yet.

    A writer still holding the file, or a table bruin has not created yet, is a
    "not yet" rather than a failure.
    """
    try:
        con = duckdb.connect(WAREHOUSE, read_only=True)
    except Exception:
        return None
    try:
        found = con.execute(
            "select schema_name from duckdb_tables() where table_name = 'fct_orders'"
        ).fetchall()
        if not found:
            return None
        return con.execute(f'select count(*) from "{found[0][0]}".fct_orders').fetchone()[0]
    except Exception:
        return None
    finally:
        con.close()


print(f"expecting {want:,} rows in fct_orders", flush=True)

seen = None
deadline = time.time() + TIMEOUT
while time.time() < deadline:
    seen = fct_rows()
    print(f"  fct_orders: {seen if seen is not None else 'not built yet'}", flush=True)
    if seen == want:
        print(f"fct_orders holds {seen:,} rows, one per order")
        sys.exit(0)
    time.sleep(10)

print(f"::error::fct_orders holds {seen} rows after {TIMEOUT}s, expected {want}")
sys.exit(1)
