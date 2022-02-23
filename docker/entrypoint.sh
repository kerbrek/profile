#!/bin/bash

./docker/wait-for-it.sh "${POSTGRES_HOST}:${POSTGRES_PORT}"

echo Migrating database...
alembic upgrade head

exec "$@"
