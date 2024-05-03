import logging
import typing
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from repository.database import async_db


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with async_db.async_session() as session:
        try:
            yield session
        except Exception as e:
            logging.error(e)
            await session.rollback()


class DbSession(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        with_session = get_flag(data, "with_session", default=False)
        if not with_session:
            try:
                result = await handler(event, data)
            except TypeError as e:
                logging.warning("If session is used, make sure you use the 'with_session' flag")
                logging.error(e)
                return
            return result

        async for async_session in get_async_session():
            data['session'] = async_session
            return await handler(event, data)
