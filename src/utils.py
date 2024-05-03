import logging
from repository.events import inspect_db_server_on_connection, inspect_db_server_on_close

from repository.database import async_db


async def start_with() -> None:
    logging.warning("Bot has been started!")


async def stop_with():
    await async_db.async_engine.dispose()
    logging.warning("Bot has been stopped!")
