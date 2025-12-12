#!/bin/sh
set -e

# Substitute environment variables in the template and output to .bruin.yml
envsubst < /bruin/bruin.yml.template > /bruin/.bruin.yml

git init .

bruin run ./ecommerce/pipeline.yml

tail -f /dev/null