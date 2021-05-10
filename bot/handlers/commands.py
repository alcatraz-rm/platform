from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp
from bot.states import RegistrationProcessStates, NewQuestionStates
import bot.keyboards.replay as kb
from bot.db.services import account_service


@dp.message_handler(commands=["exit"], state=RegistrationProcessStates.all_states)
async def handle_exit(message: types.Message, state: FSMContext):
    await message.answer(constants.REGISTRATION_CANCELED_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())
    await state.reset_data()
    await state.finish()


@dp.message_handler(commands=["new"], state="*")
async def handle_new(message: types.Message):
    if account_service.is_user_exist(t_id=message.from_user.id):
        await message.answer("Выберите тип.", reply_markup=kb.get_question_type_km())
        await NewQuestionStates.waiting_for_type.set()
    else:
        await message.answer("Зарегестрируйтесь, чтобы задать вопрос или создать обсуждение.")


@dp.message_handler(commands=["register"], state="*")
async def handle_register(message: types.Message):
    """
        This handler will be called when user sends `/register` command
        Check if user is registered.
    """

    if account_service.is_user_exist(t_id=message.from_user.id):
        await message.answer(constants.WELCOME_MESSAGE)
    else:
        await message.answer("Say your name!" + constants.REGISTRATION_EXIT_SENTENCES,
                             reply_markup=kb.ReplyKeyboardRemove())
        await RegistrationProcessStates.waiting_for_name.set()


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
    if account_service.is_user_exist(message.from_user.id):
        await message.answer(constants.HELP_MESSAGE)
    else:
        await message.answer('Who da fuck r u?', reply_markup=kb.ReplyKeyboardRemove())
        await handle_register(message)

