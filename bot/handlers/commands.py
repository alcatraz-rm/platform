from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp
from bot.states import RegistrationProcessStates
import bot.keyboards.replay as kb
from bot.db.services import account_service


'''
    Getting current state 'name':
        cs = await state.get_state()
        print(cs.split(':')[1])
'''


@dp.message_handler(commands=["exit"], state=RegistrationProcessStates.all_states)
async def handle_exit(message: types.Message, state: FSMContext):
    await message.answer(constants.REGISTRATION_CANCELED_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())
    await state.reset_data()
    await state.finish()


@dp.message_handler(state=RegistrationProcessStates.waiting_for_degree_level)
async def registration_complete(message: types.Message, state: FSMContext):
    telegram_data = message.from_user
    user_data = await state.get_data()
    user_data['degree_level'] = message.text
    # TODO: FIX how department and degree_level are being saved.
    account_service.add_new_user(t_id=telegram_data.id,
                                 t_username=telegram_data.username,
                                 name=user_data['name'],
                                 email=user_data['email'],
                                 department=user_data['department'],
                                 degree_level=user_data['degree_level'],
                                 )
    await message.answer("Регистрация прошла успешно! Добро пожаловать!", reply_markup=kb.ReplyKeyboardRemove())
    await state.finish()
    await send_welcome(message)


@dp.message_handler(state=RegistrationProcessStates.waiting_for_department)
async def registration_department(message: types.Message, state: FSMContext):
    await state.update_data(department=message.text)
    await message.answer("На каком ты уровне обучения?" + constants.REGISTRATION_EXIT_SENTENCES,
                         reply_markup=kb.get_degree_km())
    await RegistrationProcessStates.next()


@dp.message_handler(state=RegistrationProcessStates.waiting_for_email)
async def registration_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)

    await message.answer("С какого ты факультета?" + constants.REGISTRATION_EXIT_SENTENCES,
                         reply_markup=kb.get_department_km())
    await RegistrationProcessStates.next()


@dp.message_handler(state=RegistrationProcessStates.waiting_for_name)
async def registration_name(message: types.Message, state: FSMContext):
    await state.set_data({'name': message.text, })
    await message.answer("Твой адрес эл. почты (только для лохов из НГУ)." + constants.REGISTRATION_EXIT_SENTENCES,
                         reply_markup=kb.ReplyKeyboardRemove())
    await RegistrationProcessStates.next()


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

