import os

from dataclasses import dataclass

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from redis import asyncio as aioredis

from arq.connections import RedisSettings

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@dataclass
class HelpConfig:
    admin: str | None = os.getenv('ADMIN')
    support: str | None = os.getenv('SUPPORT')


@dataclass
class DatabaseConfig:
    url: str = os.getenv('URL_DB')
#     host: str | None = os.getenv('MY_DB_HOST')
#     port: int | None = int(os.getenv('MY_DB_PORT'))
#     user: str | None = os.getenv('MY_DB_USER')
#     password: str | None = os.getenv('MY_DB_PASSWORD')
#     database: str | None = os.getenv('MY_DB_DATABASE')



@dataclass
class RedisConfig:
    db: int = int(os.getenv('REDIS_DB', 1))
    host: str = os.getenv('REDIS_HOST', 'redis')
    port: int = int(os.getenv('REDIS_PORT', 6379))
    password: str = os.getenv('REDIS_PASSWORD')
    username: str = os.getenv('REDIS_USERNAME')
    state_ttl: int = os.getenv('REDIS_TTL_STATE', None)
    data_ttl: int = os.getenv('REDIS_TTL_DATA', None)

    pool_settings = RedisSettings(host=host, port=port, database=db)


redis = aioredis.Redis()
dp = Dispatcher(storage=RedisStorage(redis=redis))
bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
