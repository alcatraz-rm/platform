from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp, ADMINS_IDS
from bot.states import RegistrationProcessStates, NewQuestionStates, AdminPanelStates, InterestsInputStates, QuestionDetailStates
import bot.keyboards.replay as kb
from bot.db.services import account_service, queston_service
from bot.handlers.commands import send_welcome, handle_admin
from bot.constants import *
from bot.utils import remove_non_service_data

'''
    Getting current state 'name':
        cs = await state.get_state()
        print(cs.split(':')[1])
'''


@dp.message_handler(state=QuestionDetailStates.waiting_for_response)
async def handle_response_body(message: types.Message, state: FSMContext):
    data = await state.get_data()
    problem_id = data["problem_id"]
    response_body = message.text
    user_t_id = message.from_user.id
    queston_service.add_new_response(problem_id=problem_id,
                                     body=response_body,
                                     user_t_id=user_t_id,
                                     is_anonymous=False)
    await state.set_data(remove_non_service_data(data))
    # ???
    await send_welcome(message)


@dp.message_handler(user_id=ADMINS_IDS, state=AdminPanelStates.waiting_for_subject)
async def handle_admin_add_subject(message: types.Message, state: FSMContext):
    subject = message.text
    # go to science selection and save subject here
    await state.update_data(subject=subject)
    await message.answer("Выберите науку из списка.", reply_markup=kb.get_science_list_km())
    await state.set_state(AdminPanelStates.waiting_for_science)


@dp.message_handler(user_id=ADMINS_IDS, state=AdminPanelStates.waiting_for_science)
async def handle_admin_add_science(message: types.Message, state: FSMContext):
    science = message.text
    data = await state.get_data()

    subject = data.get('subject')
    if subject is not None:
        # checking if its from handle_admin_add_subject
        # save subject in db
        try:
            queston_service.add_new_subject(name=subject, science_name=science)
            await message.answer(
                "Наука {} выбрана для предмета \"{}\". Возвращение к админ-панели".format(science, subject),
                reply_markup=kb.ReplyKeyboardRemove())
        except queston_service.DoesNotExist:
            await message.answer("Ошибка! Что-то пошло не так...", reply_markup=kb.ReplyKeyboardRemove())

        await state.set_data(remove_non_service_data(data))
        await state.set_state(AdminPanelStates.waiting_for_command)
        await handle_admin(message, state)

    else:
        # save science in db
        queston_service.add_new_science(name=science)
        await message.answer("Наука \"{}\" добавлена.".format(science), reply_markup=kb.ReplyKeyboardRemove())
        await state.set_data(remove_non_service_data(data))
        await state.set_state(AdminPanelStates.waiting_for_command)
        await handle_admin(message, state)


@dp.message_handler(state=InterestsInputStates.waiting_for_subject)
async def add_interests_subject(message: types.Message, state: FSMContext):
    data = await state.get_data()
    science_name = data['science_name']
    subject_name = message.text
    if queston_service.is_valid(queston_service.Subject, subject_name):
        user_obj = account_service.get_user(t_id=message.from_user.id)
        account_service.assign_interest(user_obj, subject_name)
        await message.answer(constants.SETTINGS_ADD_FINISH_MESSAGE.format(interest=subject_name) +
                             "\nДля выхода напишите /exit.",
                             reply_markup=kb.get_science_list_km())
        await InterestsInputStates.waiting_for_science.set()
    else:
        await message.answer("Ошибка! Такого предмета нет. Выбири из списка.",
                             reply_markup=kb.get_subject_list_km(science=science_name))


@dp.message_handler(state=InterestsInputStates.waiting_for_science)
async def add_interests_science(message: types.Message, state: FSMContext):
    science_name = message.text
    if queston_service.is_valid(queston_service.Science, science_name):
        await state.update_data(science_name=science_name)
        await message.answer("Предмет", reply_markup=kb.get_subject_list_km(science=science_name,
                                                                            exclude_list=account_service
                                                                            .get_all_interests_for_user(
                                                                                message.from_user.id)))
        await InterestsInputStates.waiting_for_subject.set()
    else:
        await message.answer("Ошибка! Такой науки нет. Выбири из списка.",
                             reply_markup=kb.get_science_list_km())


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
        await message.answer(NEW_INCORRECT_TYPE, reply_markup=kb.get_question_type_km())
        return

    answer = ''
    if message.text == 'Вопрос':
        await state.set_data({'type': 'question'})
        answer = NEW_QUESTION_MESSAGE
    elif message.text == 'Обсуждение':
        await state.set_data({'type': 'discussion'})
        answer = NEW_DISCUSSION_MESSAGE

    await message.answer(answer, reply_markup=kb.get_exit_km())
    await NewQuestionStates.next()


@dp.message_handler(state=NewQuestionStates.waiting_for_title)
async def new_question_title(message: types.Message, state: FSMContext):
    problem_data = await state.get_data()

    type_ = problem_data.get('type')
    await state.set_data({'title': message})

    answer = ''
    if type_ == 'question':
        answer = NEW_QUESTION_PROBLEM_MESSAGE
    elif type_ == 'discussion':
        answer = NEW_DISCUSSION_PROBLEM_MESSAGE

    await message.answer(answer, reply_markup=kb.get_exit_km())
    await NewQuestionStates.next()


@dp.message_handler(state=NewQuestionStates.waiting_for_body)
async def new_question_body(message: types.Message, state: FSMContext):
    problem_data = await state.get_data()
    type_ = problem_data.get('type')
    await state.set_data({'body': message.text})

    select_topics_message = ''
    select_science_message = ''
    if type_ == 'question':
        select_topics_message = NEW_QUESTION_THEME_MESSAGE
        select_science_message = NEW_QUESTION_SCIENCE_MESSAGE
    elif type_ == 'discussion':
        select_topics_message = NEW_DISCUSSION_THEME_MESSAGE
        select_science_message = NEW_DISCUSSION_SCIENCE_MESSAGE

    await message.answer(select_topics_message)
    await message.answer(select_science_message, reply_markup=kb.get_science_list_km())
    
    await InterestsInputStates.waiting_for_science.set()


@dp.message_handler(state=InterestsInputStates.waiting_for_science)
async def new_question_science(message: types.Message, state: FSMContext):
    sciences = queston_service.get_all_sciences()
    current_science = message.text.strip()

    if current_science not in sciences:
        pass

    problem_data = await state.get_data()
    type_ = problem_data.get('type')
    
    await state.set_data({'current_science': current_science})

    answer = ''
    if type_ == 'question':
        answer = NEW_QUESTION_DISCIPLINE_MESSAGE
    elif type_ == 'discussion':
        answer = NEW_DISCUSSION_DISCIPLINE_MESSAGE

    await message.answer(answer, reply_markup=kb.get_subject_list_km(current_science))
    await InterestsInputStates.waiting_for_subject.set()


@dp.message_handler(state=InterestsInputStates.waiting_for_subject)
async def new_question_subject(message: types.Message, state: FSMContext):
    problem_data = await state.get_data()
    science = problem_data.get('current_science')

    subjects = queston_service.get_all_subjects(science)
    current_subject = message.text.strip()

    if current_subject not in subjects:
        pass

    problem_data = await state.get_data()
    type_ = problem_data.get('type')

    if 'topics' in problem_data:
        await state.update_data(topics=problem_data.get('topics') + (science, current_subject))
    else:
        await state.set_data({'topics': [(science, current_subject)]})

    await state.update_data(current_science=None)

    new_topic_message = ''
    topics_limit = 0
    process_finished_message = ''
    if type_ == 'question':
        new_topic_message = NEW_QUESTION_THEME_SAVED_MESSAGE
        process_finished_message = NEW_QUESTION_THEME_FINISH_MESSAGE
        topics_limit = 3
    elif type_ == 'discussion':
        new_topic_message = NEW_DISCUSSION_THEME_SAVED_MESSAGE
        process_finished_message = NEW_DISCUSSION_THEME_FINISH_MESSAGE
        topics_limit = 5

    if len(problem_data.get('topics') + 1) == topics_limit:
        if type_ == 'discussion':
            await message.answer(NEW_DISCUSSION_THEME_FINISH_MESSAGE)
        elif type_ == 'question':
            await message.answer(NEW_QUESTION_THEME_FINISH_MESSAGE)
            await message.answer(NEW_QUESTION_ANON_MESSAGE, reply_markup=kb.get_yes_no_km())

            await NewQuestionStates.waiting_for_anonymous_or_not_answer.set()
        return

    await message.answer(new_topic_message, reply_markup=kb.get_add_finish_exit_km())
    await NewQuestionStates.waiting_for_new_topic_or_quit.set()


@dp.message_handler(state=NewQuestionStates.waiting_for_anonymous_or_not_answer)
async def handle_new_anonymous_question_answer(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    problem_data = await state.get_data()
    type_ = problem_data.get('type')

    if type_ == 'question':
        process_finished_message = NEW_QUESTION_END_MESSAGE
    else:
        process_finished_message = NEW_DISCUSSION_END_MESSAGE

    if answer == 'Да':
        await state.update_data(anonymous_question=True)

        # TODO: problem saving logic
        problem_id = 0  # id from db

        await message.answer(process_finished_message.format(id=problem_id))

    elif answer == 'Нет':
        await state.update_data(anonymous_question=False)

        # TODO: problem saving logic
        problem_id = 0  # id from db

        await message.answer(process_finished_message.format(id=problem_id))
        await state.set_data(remove_non_service_data(problem_data))
        await state.reset_state(with_data=False)

    else:
        await message.answer(NEW_QUESTION_SELECT_YES_OR_NO, reply_markup=kb.get_yes_no_km())


@dp.message_handler(state="*")
async def handle_any_other_message(message: types.Message, state: FSMContext):
    await message.answer("Ошибка! Невозможно выполнить эту команду сейчас!")
    await send_welcome(message)
