#!/bin/sh
# The script expects database availability and performs migrations with alembic and setup webhooks with on_startup.py

echo "\e[96mWaiting for postgres...\e[0m"
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

set -e

echo "\e[96mPostgreSQL started, applying migrations...\e[0m"
alembic upgrade head
echo "\e[96mMigrations applied.\e[0m"

echo "\e[96mSetting WebHook...\e[0m"
python on_startup.py
echo "\e[96mWebHook has been set.\e[0m"

exec "$@"
