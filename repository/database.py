import pydantic
from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import Pool as SQLAlchemyPool

from data.config import settings


class AsyncDatabase:
    def __init__(self):
        self.postgres_uri: pydantic.PostgresDsn = settings.postgres_dsn
        self.async_engine: AsyncEngine = create_async_engine(
            url=self.set_async_db_uri,
        )
        self.async_session: AsyncSession = AsyncSession(bind=self.async_engine)
        self.pool: SQLAlchemyPool = self.async_engine.pool

    @property
    def set_async_db_uri(self) -> str | pydantic.PostgresDsn:
        return (
            self.postgres_uri.replace("postgresql://", "postgresql+asyncpg://")
            if self.postgres_uri
            else self.postgres_uri
        )


async_db: AsyncDatabase = AsyncDatabase()

redis_client: Redis = aioredis.from_url(url=settings.redis_url)
storage = RedisStorage(redis=redis_client)
