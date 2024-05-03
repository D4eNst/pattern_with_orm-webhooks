from pathlib import Path

from decouple import config
from pydantic import BaseConfig
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    """ Main settings. To manage values use .env file """

    class Config(BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True
        extra: str = 'ignore'

    # src settings
    TOKEN: str = config("TOKEN", cast=str)  # type: ignore
    ADMIN_ID: int = config("ADMIN_ID", cast=int)  # type: ignore

    REDIS_HOST: str = config("REDIS_HOST", cast=str)  # type: ignore
    REDIS_PASSWORD: str = config("REDIS_PASSWORD", cast=str)  # type: ignore
    REDIS_PORT: int = config("REDIS_PORT", cast=int)  # type: ignore

    POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str)  # type: ignore
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int)  # type: ignore
    POSTGRES_DATABASE: str = config("POSTGRES_DATABASE", cast=str)  # type: ignore
    POSTGRES_USER: str = config("POSTGRES_USER", cast=str)  # type: ignore
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str)  # type: ignore

    @property
    def redis_url(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def postgres_dsn(self) -> str:
        return (f"postgresql://"
                f"{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DATABASE}")

    @property
    def postgres_dsn_to_main_db(self) -> str:
        return self.postgres_dsn.replace(self.POSTGRES_DATABASE, self.POSTGRES_MAIN)


settings = Settings()
