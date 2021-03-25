#!/usr/bin/env sh

set -o errexit
set -o nounset

/usr/local/bin/python -Wi -m celery -A project worker \
    --loglevel=INFO \
    --time-limit=43200 \
    --concurrency=8
