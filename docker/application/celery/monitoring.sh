#!/usr/bin/env sh

set -o errexit
set -o nounset


[ -z "${RABBITMQ_HOST}" ] && exit 1
[ -z "${RABBITMQ_LOGIN}" ] && exit 1
[ -z "${RABBITMQ_PASSWORD}" ] && exit 1
[ -z "${RABBITMQ_PORT}" ] && RABBITMQ_PORT=5672
[ -z "${RABBITMQ_MANAGEMENT_PORT}" ] && RABBITMQ_MANAGEMENT_PORT=15672

RABBITMQ_LOGIN_PASSWORD="${RABBITMQ_LOGIN}:${RABBITMQ_PASSWORD}"

/usr/local/bin/python -Wi -m flower -A project \
    --address=0.0.0.0 \
    --port=5555 \
    --logging=info \
    --broker="amqp://${RABBITMQ_LOGIN_PASSWORD}@${RABBITMQ_HOST}:${RABBITMQ_PORT}/video-archive" \
    --broker_api="http://${RABBITMQ_LOGIN_PASSWORD}@${RABBITMQ_HOST}:${RABBITMQ_MANAGEMENT_PORT}/api/video-archive"
