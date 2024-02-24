import asyncio
import logging

from commands import register_client_command, register_client_command_fsm, register_client_command_other

from db.engine import create_db, session_maker

from bot.middlewares.db import DataBaseSession
from bot.config import dp, bot


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    register_client_command(dp)
    register_client_command_fsm(dp)
    register_client_command_other(dp)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
