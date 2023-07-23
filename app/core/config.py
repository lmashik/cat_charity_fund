import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from pydantic import BaseSettings, EmailStr

from app.constants import BASE_DIR, DT_FORMAT, LOG_FORMAT


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд QRKot'
    app_description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()


def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'qrkot.log'
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
