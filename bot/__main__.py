import asyncio
import logging

from aiogram.types import BotCommandScopeAllPrivateChats

from arq import create_pool
from arq.connections import RedisSettings


from bot.db.engine import create_db, session_maker
from bot.commands import register_client_command, register_client_command_fsm, register_client_command_other
from bot.middlewares.db import DataBaseSession
from bot.config import bot, dp
from bot.common.bot_cmd_lst import bot_cmd_lst


async def main() -> None:

    logging.basicConfig(level=logging.DEBUG)

    register_client_command(dp)
    register_client_command_fsm(dp)
    register_client_command_other(dp)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    redis_pool = await create_pool(RedisSettings())
    await create_db()
    await bot.set_my_commands(commands=bot_cmd_lst, scope=BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, arqredis=redis_pool)


if __name__ == '__main__':
    asyncio.run(main())
