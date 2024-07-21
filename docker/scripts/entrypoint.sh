#!/bin/sh

set -o errexit
set -o nounset

readonly cmd="$*"

# The script expects database availability and performs migrations with alembic and setup webhooks with on_startup.py
echo "\e[96mWaiting for postgres...\e[0m"
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "\e[96mPostgreSQL started\e[0m"

set -e

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
