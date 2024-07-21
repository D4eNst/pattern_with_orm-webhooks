from pathlib import Path

from pydantic import (
    Field,
    PostgresDsn,
    RedisDsn,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_base_dir() -> Path:
    print(Path(__file__).parent.parent.resolve())
    return Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    """ Main settings. To manage values use .env file """
    ROOT_DIR: Path = Path(__file__).parent.parent.resolve()

    # app settings
    DOMAIN: str
    WEBHOOK_PATH: str
    DEBUG: bool = False

    # src settings
    TOKEN: str
    ADMIN_ID: int

    # Redis settings
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int

    # Postgres settings
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def redis_url(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT
        )

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE
        )

    @property
    def set_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values.
        """
        return {
            "title": "Bot",
            "version": "0.1.0",
            # "debug": self.DEBUG,
            # "description": self.DESCRIPTION,
            # "docs_url": self.DOCS_URL,
            # "openapi_url": self.OPENAPI_URL,
            # "redoc_url": self.REDOC_URL,
            # "openapi_prefix": self.OPENAPI_PREFIX,
            # "api_prefix": self.API_PREFIX,
        }

    model_config = SettingsConfigDict(
        case_sensitive=True,
        validate_assignment=True,
        extra="ignore",
        env_file=ROOT_DIR / ".env",
    )


settings = Settings()
