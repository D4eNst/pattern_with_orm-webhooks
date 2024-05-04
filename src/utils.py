from bot import bot
from repository.database import async_db
# use this import for register events for database
# from repository.events import inspect_db_server_on_connection, inspect_db_server_on_close
from repository.events import inspect_db_server_on_connection, inspect_db_server_on_close  # type: ignore


async def app_start_with() -> None:
    async with async_db.async_engine.connect():
        # check connection
        pass


async def app_stop_with() -> None:
    await bot.session.close()
    await async_db.async_engine.dispose()
