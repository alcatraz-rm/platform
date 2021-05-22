import sys

sys.path.append('..')

from bot.config import dp, executor, displayed_commands, bot
from aiogram import Dispatcher
from bot.db import helper
from bot.handlers import commands, messages


async def on_startup(dp: Dispatcher):
    """
        Creates tables if they don't exist.
    """
    helper.create_tables()
    await bot.set_my_commands(commands=displayed_commands)


async def on_shutdown(dp: Dispatcher):
    helper.db.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    print("shutdown")


if __name__ == '__main__':
    # helper.migrate_db()
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
    executor.start_polling(dp)
