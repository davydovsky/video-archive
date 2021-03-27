#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

db_ready () {
  # Check that db is up and running on port `3306`:
  dockerize -wait 'tcp://db:3306' -timeout 5s
}

rabbitmq_ready () {
  # Check that rabbitmq is up and running on port `15672`:
  dockerize -wait 'http://rabbitmq:15672' -timeout 5s
}

until db_ready; do
  >&2 echo 'Database is unavailable - sleeping'
done
>&2 echo 'Database is up - continuing...'

until rabbitmq_ready; do
  >&2 echo 'RabbitMQ is unavailable - sleeping'
done
>&2 echo 'RabbitMQ is up - continuing...'


# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
