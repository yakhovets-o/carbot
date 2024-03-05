import asyncio
import logging.config

from aiogram.types import BotCommandScopeAllPrivateChats
from arq import create_pool
from arq.connections import RedisSettings

from bot.commands import register_client_command, register_client_command_fsm, register_client_command_other
from bot.common.bot_cmd_lst import bot_cmd_lst
from bot.config import bot, dp
from bot.db.engine import create_db, session_maker
from bot.logger_conf.logger_conf import get_logg_conf
from bot.middlewares.db import DataBaseSession


logging.config.dictConfig(get_logg_conf())

loger = logging.getLogger(__name__)


async def main() -> None:
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
