import asyncio
from logging.config import dictConfig

from aiogram.methods import DeleteWebhook

from bot import dp, bot
from content.handlers.routs import main_router
from content.middlewares.middleware import register_middlewares
from logs import logging_config
from management import app_start_with, app_stop_with

dictConfig(logging_config)


async def start_bot():
    # register handlers and start/stop functions
    register_middlewares(dp)
    dp.include_router(main_router)

    dp.startup.register(app_start_with)
    dp.shutdown.register(app_stop_with)

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
