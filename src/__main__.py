import asyncio
import logging

from aiogram.methods import DeleteWebhook

from repository.database import async_db

from src.bot import dp, bot
from src.content.handlers.routs import (
    basic_router
)
from src.content.middlewares.middleware import rg_middlewares
from src.utils import start_with, stop_with

logging.basicConfig(level=logging.INFO)


async def start_bot():
    # register handlers and start/stop functions

    dp.include_routers(
        basic_router
    )

    dp.startup.register(start_with)
    dp.shutdown.register(stop_with)

    rg_middlewares(dp)

    try:
        async with async_db.async_engine.connect():
            # check connection, apply migrations
            pass
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
