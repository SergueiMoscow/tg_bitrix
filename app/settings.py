import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str = ''

    ROOT_DIR: Path = ROOT_DIR
    DB_DSN: str = ''
    DATABASE_SCHEMA: str = 'main'
    MAX_COUNT: int = 50
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / '.env',
        env_file_encoding='utf-8',
        extra='allow',
    )


settings = Settings()
