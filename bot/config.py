import os

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from redis import asyncio as aioredis

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

admin = os.getenv('ADMIN')
support = os.getenv('SUPPORT')

db_host = os.getenv('MY_DB_HOST')
db_port = os.getenv('MY_DB_PORT')
db_user = os.getenv('MY_DB_USER')
db_password = os.getenv('MY_DB_PASSWORD')
db_database = os.getenv('MY_DB_DATABASE')

redis = aioredis.Redis()
dp = Dispatcher(storage=RedisStorage(redis=redis))
bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
