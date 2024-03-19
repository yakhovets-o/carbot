import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommandScopeAllPrivateChats
from arq import create_pool
from arq.connections import RedisSettings
from redis import asyncio as aioredis

from bot.commands import register_client_command, register_client_command_fsm, register_client_command_other
from bot.common.bot_cmd_lst import bot_cmd_lst
from bot.config import BotConfig
from bot.db.engine import create_db, session_maker
from bot.logger_conf.logger_conf import get_logg_conf
from bot.middlewares.db import DataBaseSession


logging.config.dictConfig(get_logg_conf())

loger = logging.getLogger(__name__)


async def main() -> None:

    redis = aioredis.Redis()
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    bot = Bot(token=BotConfig.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    register_client_command(dp)
    register_client_command_fsm(dp)
    register_client_command_other(dp)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    redis_pool = await create_pool(RedisSettings())

    await create_db()

    await bot.set_my_commands(commands=bot_cmd_lst, scope=BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, arqredis=redis_pool)


if __name__ == "__main__":
    asyncio.run(main())
