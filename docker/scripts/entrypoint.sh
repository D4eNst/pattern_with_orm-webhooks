#!/bin/sh


# The script expects database availability and performs migrations with alembic and setup webhooks with on_startup.py
printf "\e[96mWaiting for postgres...\e[0m"
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

set -e

printf "\e[96mPostgreSQL started, applying migrations...\e[0m"
alembic upgrade head
printf "\e[96mMigrations applied.\e[0m"

printf "\e[96mSetting WebHook...\e[0m"
python management.py
printf "\e[96mWebHook has been set.\e[0m"

exec "$@"
