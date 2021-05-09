from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext


from bot import constants
from bot.config import dp
from bot.states import RegistrationProcessStates

from bot.db.services import account_service


@dp.message_handler(commands=["register"], state="*")
async def handle_register(message: types.Message, state: FSMContext):
    """
        This handler will be called when user sends `/register` command
        Check if user is registered.
    """
    if account_service.is_user_exist(t_id=message.from_user.id):
        await message.answer(constants.WELCOME_MESSAGE)
    else:
        await message.answer("Who the fuck are you?")


@dp.message_handler(commands=["help"], state="*")
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """

    await message.answer(constants.HELP_MESSAGE)


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """

    await message.answer(constants.HELP_MESSAGE)

