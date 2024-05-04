import logging

from aiogram.methods import DeleteWebhook

from data.config import settings
from repository.events import inspect_db_server_on_connection, inspect_db_server_on_close

from repository.database import async_db
from src.bot import bot


async def app_start_with() -> None:
    async with async_db.async_engine.connect():
        # check connection
        pass

    await bot(DeleteWebhook(drop_pending_updates=True))
    webhook_url = f"{settings.DOMAIN}{settings.WEBHOOK_PATH}"
    await bot.set_webhook(url=webhook_url)


async def app_stop_with() -> None:
    await bot.session.close()
    await async_db.async_engine.dispose()
