#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

db_ready () {
  # Check that db is up and running on port `3306`:
  dockerize -wait 'tcp://db:3306' -timeout 5s
}

# We need this line to make sure that this container is started
# after the one with Database:
until db_ready; do
  >&2 echo 'Database is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Database is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
