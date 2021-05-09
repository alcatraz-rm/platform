from bot.config import dp, executor
from aiogram import Dispatcher
from bot.db import helper
from bot.handlers import commands, messages


async def on_startup(dp: Dispatcher):
    """
        Creates tables if they don't exist.
    """
    helper.create_tables()


async def on_shutdown(dp: Dispatcher):
    helper.db.close()


if __name__ == '__main__':
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
    executor.start_polling(dp)
