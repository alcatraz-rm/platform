import os
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot.middlewares import StateValidationMiddleware

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import Executor


# Getting envs
API_TOKEN = os.getenv("API_TOKEN")
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# Cfg related constants
ADMINS_IDS = [401961508, 187289003]

displayed_commands = [
    types.BotCommand(command="/help", description="Список доступынх команд"),
    types.BotCommand(command="/new", description="Создание нового вопроса"),
    types.BotCommand(command="/feed", description="Лента вопросов"),
    types.BotCommand(command="/detail", description="Детализация вопроса"),
    types.BotCommand(command="/me", description="Личные данные"),
    types.BotCommand(command="/settings", description="Настройки профиля"),
    types.BotCommand(command="/about", description="Информация о боте"),
]


# Configure logging
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)


storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(StateValidationMiddleware())
executor = Executor(dp, skip_updates=True)

