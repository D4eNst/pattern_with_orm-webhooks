import logging
import typing
from typing import Callable, Awaitable, Dict, Any
from aiogram.types.base import TelegramObject
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from repository.database import async_db


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    try:
        yield async_db.async_session
    except Exception as e:
        logging.error(e)
        await async_db.async_session.rollback()
    finally:
        await async_db.async_session.close()


class DbSession(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async for async_session in get_async_session():
            data['session'] = async_session
            return await handler(event, data)
