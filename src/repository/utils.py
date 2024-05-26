import functools
import logging
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from repository.database import async_db
from repository.models.base import Base


async def create_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with async_db.async_session() as session:
        try:
            yield session
        except Exception as e:
            logging.error(e)
            await session.rollback()


def get_async_session(func):
    """Decorator that creates an asynchronous session and passes it to the function parameters"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if kwargs.get('session', None) is None:
            async for session in create_async_session():
                kwargs['session'] = session
                return await func(*args, **kwargs)
        return await func(*args, **kwargs)

    return wrapper


def get_model_by_name(name: str) -> Base | None:
    models_dict = {
        mapper_cls.class_.__name__: mapper_cls.class_
        for mapper_cls in Base.registry.mappers
    }

    return models_dict.get(name)
