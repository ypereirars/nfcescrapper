from functools import lru_cache
import os

from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI")
    DATABASE_DIALECT: str = os.getenv("DATABASE_DIALECT", "postgresql")
    DATABASE_HOSTNAME: str = os.getenv("DATABASE_HOSTNAME", "localhost")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT", 5432)
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME", "")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", False)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
