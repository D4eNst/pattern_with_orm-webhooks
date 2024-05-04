from typing import Any

from aiogram import types
from fastapi import APIRouter, status

from data.config import settings
from src.bot import dp, bot

router = APIRouter(prefix=settings.WEBHOOK_PATH, tags=["webhooks"])


@router.post(path="", status_code=status.HTTP_200_OK)
async def webhook(update: dict[str, Any]) -> None:
    try:
        await dp.feed_webhook_update(bot=bot, update=types.Update(**update))
    except Exception as e:
        # logging.exception(e)
        pass
