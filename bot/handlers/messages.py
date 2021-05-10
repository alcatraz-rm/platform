from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp
from bot.states import RegistrationProcessStates, NewQuestionStates
import bot.keyboards.replay as kb
from bot.db.services import account_service
from bot.handlers.commands import send_welcome

'''
    Getting current state 'name':
        cs = await state.get_state()
        print(cs.split(':')[1])
'''


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


# /new process

@dp.message_handler(state=NewQuestionStates.waiting_for_type)
async def new_question_type(message: types.Message, state: FSMContext):
    if message.text not in ['Вопрос', 'Обсуждение']:
        await message.answer('Выбери корректный тип, используя клавиатуру.', reply_markup=kb.get_question_type_km())
        return

    answer = ''
    if message.text == 'Вопрос':
        await state.set_data({'type': 'question'})
        answer = 'Введи название вопроса. Постарайся быть максмально конкретным.'
    elif message.text == 'Обсуждение':
        await state.set_data({'type': 'discussion'})
        answer = 'Введи название обсуждения. Постарайся быть максмально конкретным.'

    await message.answer(answer)
    await NewQuestionStates.next()


@dp.message_handler(state=NewQuestionStates.waiting_for_title)
async def new_question_title(message: types.Message, state: FSMContext):
    pass

