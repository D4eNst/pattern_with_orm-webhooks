from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject

from repository.utils import create_async_session


class DbSession(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async for async_session in create_async_session():
            data['session'] = async_session
            return await handler(event, data)
