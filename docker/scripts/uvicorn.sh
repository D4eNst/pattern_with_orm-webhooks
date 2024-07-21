#!/bin/sh

set -o errexit
set -o nounset

readonly cmd="$*"

# Check that $BOT_ENV is set to "production",
# fail otherwise, since it may break things:

echo "BOT_ENV is $BOT_ENV"
if [ "$BOT_ENV" != 'production' ]; then
  echo 'Error: BOT_ENV is not set to "production".'
  echo 'Application will not start.'
  exit 1
fi

export BOT_ENV

# Applying migrations and setting webhooks:
echo "Applying migrations..."
alembic upgrade head
echo "Migrations applied."

echo "Setting WebHook..."
python management.py
echo "WebHook has been set."

# Start uvicorn:
uvicorn webhook_main:app --host 0.0.0.0 --port 8080 --workers 4

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
