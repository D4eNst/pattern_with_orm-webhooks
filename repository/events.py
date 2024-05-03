import logging

from alembic import command
from alembic.config import Config

from repository.database import async_db
from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_connection
from sqlalchemy.pool import _ConnectionRecord


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="connect")
def inspect_db_server_on_connection(
        db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
) -> None:
    logging.info(f"New DB API Connection ---\n {db_api_connection}")
    logging.info(f"Connection Record ---\n {connection_record}")

    logging.info("Running DB migrations")
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option(name="sqlalchemy.url", value=f"{str(async_db.set_async_db_uri)}?async_fallback=True")
    command.upgrade(alembic_cfg, 'head')


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="close")
def inspect_db_server_on_close(
        db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
) -> None:
    logging.info(f"Closing DB API Connection ---\n {db_api_connection}")
    logging.info(f"Closed Connection Record ---\n {connection_record}")
