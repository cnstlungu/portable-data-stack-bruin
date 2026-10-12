#!/bin/sh
set -e

# Substitute environment variables in the template and output to .bruin.yml
envsubst < /bruin/bruin.yml.template > /bruin/.bruin.yml

git init .

# One asset at a time. Every asset writes the same DuckDB file, and DuckDB lets
# only one process hold it: with bruin's default 16 workers, an ingestr load
# could start while bruin itself had the file open for a SQL asset, and fail
# with "Could not set lock on file".
bruin run --workers 1 ./ecommerce/pipeline.yml

tail -f /dev/null