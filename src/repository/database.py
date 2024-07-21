import pydantic
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import Pool
from yarl import URL

from data.config import settings


class AsyncDatabase:
    def __init__(self):
        self.__postgres_dsn: pydantic.PostgresDsn = settings.postgres_dsn
        self.async_engine: AsyncEngine = create_async_engine(
            url=self.async_postgres_dsn,
        )
        self.async_session = async_sessionmaker(self.async_engine, expire_on_commit=False)
        self.pool: Pool = self.async_engine.pool

    @property
    def async_postgres_dsn(self) -> str:
        url = URL(self.__postgres_dsn.unicode_string())
        async_url = url.with_scheme("postgresql+asyncpg")
        return str(async_url)

    @property
    def sync_postgres_dsn(self) -> str:
        return self.__postgres_dsn.unicode_string()


async_db: AsyncDatabase = AsyncDatabase()
