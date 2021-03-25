#!/usr/bin/env sh

set -o errexit
set -o nounset

/usr/local/bin/python -Wi -m celery inspect ping -A project
