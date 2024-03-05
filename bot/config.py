import os
from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from arq.connections import RedisSettings
from dotenv import find_dotenv, load_dotenv
from redis import asyncio as aioredis


load_dotenv(find_dotenv())


@dataclass
class HelpConfig:
    admin: str | None = os.getenv("ADMIN")
    support: str | None = os.getenv("SUPPORT")


@dataclass
class DatabaseConfig:
    url: str = os.getenv("URL_DB")


@dataclass
class RedisConfig:
    pool_settings = RedisSettings()


@dataclass
class BotConfig:
    token: str = os.getenv("TOKEN")


redis = aioredis.Redis()
dp = Dispatcher(storage=RedisStorage(redis=redis))
bot = Bot(token=os.getenv("TOKEN"), parse_mode=ParseMode.HTML)
