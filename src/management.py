import asyncio
import logging

from aiogram.methods import DeleteWebhook
from aiogram.types import WebhookInfo

from bot import bot
from data.config import settings
from repository.database import async_db
from repository.events import inspect_db_server_on_connection, inspect_db_server_on_close  # type: ignore

loger = logging.getLogger(__name__)


async def app_start_with() -> None:
    async with async_db.async_engine.connect():
        # check connection
        pass


async def app_stop_with() -> None:
    await bot.session.close()
    await async_db.async_engine.dispose()


async def set_webhook_on_startup() -> None:
    webhook_info: WebhookInfo = await bot.get_webhook_info()
    print(webhook_info)

    await bot(DeleteWebhook(drop_pending_updates=True))
    webhook_url = f"https://{settings.DOMAIN}{settings.WEBHOOK_PATH}"

    webhook_info: WebhookInfo = await bot.get_webhook_info()
    print(webhook_info)

    if webhook_info.url != webhook_url:
        print("YES")
        await bot.set_webhook(
            url=webhook_url,
            # allowed_updates=["message", "callback_query"]
        )
    await bot.session.close()


if __name__ == '__main__':
    asyncio.run(set_webhook_on_startup())
