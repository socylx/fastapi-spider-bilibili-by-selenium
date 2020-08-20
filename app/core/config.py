import logging
import sys
from typing import List


from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings

from app.core.logging import InterceptHandler

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Bearer"
VERSION = "0.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE: str = config("DATABASE", cast=str)
DATABASE_URL: str = config("DB_CONNECTION", cast=str)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

PROJECT_NAME: str = config("PROJECT_NAME", default="BiliBili")

ALLOWED_HOSTS: List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]

for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[
    {
        "sink": sys.stderr,
        "level": LOGGING_LEVEL
    }
])

USERS_COLLECTION_NAME: str = config("USERS_COLLECTION_NAME", cast=str, default="users")

UP_COLLECTION_NAME: str = config("UP_COLLECTION_NAME", cast=str, default="test")
UP_VIDEO_COLLECTION_NAME: str = config("UP_VIDEO_COLLECTION_NAME", cast=str, default="test")
UP_AUDIO_COLLECTION_NAME: str = config("UP_AUDIO_COLLECTION_NAME", cast=str, default="test")
UP_ARTICLE_COLLECTION_NAME: str = config("UP_ARTICLE_COLLECTION_NAME", cast=str, default="test")
UP_ALBUM_COLLECTION_NAME: str = config("UP_ALBUM_COLLECTION_NAME", cast=str, default="test")

TXT_DIR_PATH: str = config("TXT_DIR_PATH", cast=str, default="D:\Coding\\bilibili\\txt")
