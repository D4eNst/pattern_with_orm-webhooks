import asyncio

from aiogram.methods import DeleteWebhook

from bot import bot
from data.config import settings


async def on_startup() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    webhook_url = f"{settings.DOMAIN}{settings.WEBHOOK_PATH}"
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != webhook_url:
        await bot.set_webhook(
            url=webhook_url,
            # allowed_updates=["message", "callback_query"]
        )
    await bot.session.close()


if __name__ == '__main__':
    asyncio.run(on_startup())
