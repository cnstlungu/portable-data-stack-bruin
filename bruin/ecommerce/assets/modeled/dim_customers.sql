/* @bruin
name: dim_customers
type: duckdb.sql
materialization:
   type: table
depends:
   - raw.customers

columns:
  - name: customer_id
    type: varchar
    description: "Unique customer identifier"
    checks:
      - name: not_null
      - name: unique
  - name: email
    type: varchar
    description: "Customer email address"
    checks:
      - name: not_null
      - name: pattern
        value: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  - name: name
    type: varchar
    checks:
      - name: not_null

custom_checks:
  - name: created_before_updated
    query: |
      SELECT COUNT(*) as issue_count
      FROM dim_customers
      WHERE created_at > updated_at
    value: 0

@bruin */

SELECT 
    id AS customer_id,
    email,
    name,
    country,
    city,
    created_at,
    updated_at
FROM raw.customers
