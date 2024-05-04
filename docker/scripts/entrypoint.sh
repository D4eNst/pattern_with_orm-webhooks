#!/bin/sh
# The script expects database availability and performs migrations with alembic.

echo "\e[96mWaiting for postgres...\e[0m"
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

set -e

echo "\e[96mPostgreSQL started, applying migrations...\e[0m"
alembic upgrade head
echo "\e[96mMigrations applied.\e[0m"

exec "$@"
