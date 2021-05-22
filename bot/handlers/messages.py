from aiogram import types
from aiogram.dispatcher import FSMContext

import bot.keyboards.replay as kb
from bot import constants
from bot.config import dp, ADMINS_IDS
from bot.constants import *
from bot.db.services import account_service, queston_service
from bot.db.services.queston_service import add_new_problem, assign_topic
from bot.handlers.commands import send_welcome, handle_admin, handle_detail
from bot.states import RegistrationProcessStates, NewQuestionStates, AdminPanelStates, InterestsInputStates, \
    SettingsChangeStates, QuestionDetailStates
from bot.utils import remove_non_service_data

'''
    Getting current state 'name':
        cs = await state.get_state()
        print(cs.split(':')[1])
'''



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


# /settings process:

@dp.message_handler(state=SettingsChangeStates.waiting_for_name)
async def handle_settings_option(message: types.Message):
    user = account_service.get_user(message.from_user.id)
    account_service.alter_user_info(user, name=message.text)
    await message.answer(SETTINGS_NAME_CHANGED_MESSAGE.format(name=message.text))
    await message.answer(constants.SETTINGS_MESSAGE, reply_markup=kb.get_settings_option_km())
    await SettingsChangeStates.waiting_for_option.set()


@dp.message_handler(state=SettingsChangeStates.waiting_for_department)
async def handle_settings_option(message: types.Message):
    user = account_service.get_user(message.from_user.id)
    account_service.alter_user_info(user, department=message.text)
    await message.answer(SETTINGS_FACULTY_CHANGED_MESSAGE.format(faculty=message.text))
    await message.answer(constants.SETTINGS_MESSAGE, reply_markup=kb.get_settings_option_km())
    await SettingsChangeStates.waiting_for_option.set()


@dp.message_handler(state=SettingsChangeStates.waiting_for_degree_level)
async def handle_settings_option(message: types.Message):
    user = account_service.get_user(message.from_user.id)
    account_service.alter_user_info(user, degree_level=message.text)
    await message.answer(SETTINGS_DEGREE_CHANGED_MESSAGE.format(degree=message.text))
    await message.answer(constants.SETTINGS_MESSAGE, reply_markup=kb.get_settings_option_km())
    await SettingsChangeStates.waiting_for_option.set()


@dp.message_handler(state=SettingsChangeStates.waiting_for_new_subject)
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
        await SettingsChangeStates.waiting_for_new_science.set()
    else:
        await message.answer("Ошибка! Такого предмета нет. Выбири из списка.",
                             reply_markup=kb.get_subject_list_km(science=science_name))


@dp.message_handler(state=SettingsChangeStates.waiting_for_new_science)
async def add_interests_science(message: types.Message, state: FSMContext):
    science_name = message.text
    if queston_service.is_valid(queston_service.Science, science_name):
        await state.update_data(science_name=science_name)
        await message.answer("Предмет", reply_markup=kb.get_subject_list_km(science=science_name,
                                                                            exclude_list=account_service
                                                                            .get_all_interests_for_user(
                                                                                message.from_user.id)))
        await SettingsChangeStates.waiting_for_new_subject.set()
    else:
        await message.answer("Ошибка! Такой науки нет. Выбири из списка.",
                             reply_markup=kb.get_science_list_km())


@dp.message_handler(state=SettingsChangeStates.waiting_for_del_interest)
async def handle_deleting_interest(message: types.Message):
    user_id = message.from_user.id
    user = account_service.get_user(user_id)
    user_interests = account_service.get_all_interests_for_user(user_id)
    science_subject = message.text.split(sep='/')
    if user_interests[science_subject[0]] == science_subject[1]:
        account_service.remove_interest(user, science_subject[1])
        await message.answer(SETTINGS_DELETE_FINISH_MESSAGE.format(interest=message.text))
        await message.answer(constants.SETTINGS_MESSAGE, reply_markup=kb.get_settings_option_km())
        await SettingsChangeStates.waiting_for_option.set()
    else:
        await message.answer("Такого интереса у вас нет!")
        await message.answer(constants.SETTINGS_MESSAGE, reply_markup=kb.get_settings_option_km())
        await SettingsChangeStates.waiting_for_option.set()


@dp.message_handler(state=SettingsChangeStates.waiting_for_option)
async def handle_settings_option(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == 'Name':
        await message.answer(SETTINGS_NAME_MESSAGE)
        await SettingsChangeStates.waiting_for_name.set()
    elif message.text == 'Department':
        await message.answer(SETTINGS_FACULTY_MESSAGE, reply_markup=kb.get_department_km())
        await SettingsChangeStates.waiting_for_department.set()
    elif message.text == 'Degree':
        await message.answer(SETTINGS_DEGREE_MESSAGE, reply_markup=kb.get_degree_km())
        await SettingsChangeStates.waiting_for_degree_level.set()
    elif message.text == 'Add interest':
        await message.answer(SETTINGS_NAME_MESSAGE, reply_markup=kb.get_science_list_km())
        data = await state.get_data()
        await state.set_data(remove_non_service_data(data))
        await SettingsChangeStates.waiting_for_new_science.set()
    elif message.text == 'Delete interest':
        await message.answer(SETTINGS_DELETE_MESSAGE, reply_markup=kb.get_interests_km(user_id))
        await SettingsChangeStates.waiting_for_del_interest.set()


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
    problem_data['title'] = message.text
    await state.set_data(problem_data)

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
    problem_data['body'] = message.text

    await state.set_data(problem_data)

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

    await NewQuestionStates.waiting_for_science.set()


@dp.message_handler(state=NewQuestionStates.waiting_for_science)
async def new_question_science(message: types.Message, state: FSMContext):
    sciences = queston_service.get_all_sciences()
    current_science = message.text.strip()

    if current_science not in sciences:
        await message.answer('Такой науки нет! Выбери из списка', reply_markup=kb.get_subject_list_km(current_science))

    problem_data = await state.get_data()
    type_ = problem_data.get('type')

    problem_data['current_science'] = current_science
    await state.set_data(problem_data)

    answer = ''
    if type_ == 'question':
        answer = NEW_QUESTION_DISCIPLINE_MESSAGE
    elif type_ == 'discussion':
        answer = NEW_DISCUSSION_DISCIPLINE_MESSAGE

    await message.answer(answer, reply_markup=kb.get_subject_list_km(current_science))
    await NewQuestionStates.waiting_for_subject.set()


@dp.message_handler(state=NewQuestionStates.waiting_for_subject)
async def new_question_subject(message: types.Message, state: FSMContext):
    problem_data = await state.get_data()
    science = problem_data.get('current_science')

    subjects = queston_service.get_all_subjects(science)
    current_subject = message.text.strip()

    if current_subject not in subjects:
        await message.answer('Такого предмета нет! Выбери из списка', reply_markup=kb.get_subject_list_km(science))

    problem_data = await state.get_data()
    type_ = problem_data.get('type')

    if 'topics' in problem_data:
        problem_data['topics'] += [(science, current_subject)]
    else:
        problem_data['topics'] = [(science, current_subject)]

    await state.set_data(problem_data)
    await state.update_data(current_science=None)

    new_topic_message = ''
    topics_limit = 0
    if type_ == 'question':
        new_topic_message = NEW_QUESTION_THEME_SAVED_MESSAGE
        topics_limit = 3
    elif type_ == 'discussion':
        new_topic_message = NEW_DISCUSSION_THEME_SAVED_MESSAGE
        topics_limit = 5

    if len(problem_data.get('topics')) + 1 == topics_limit:
        if type_ == 'discussion':
            await message.answer(NEW_DISCUSSION_THEME_FINISH_MESSAGE)

            problem = add_new_problem(problem_data['title'], problem_data['body'], message.from_user.id)

            for topic in problem_data['topics']:
                assign_topic(problem, topic[1])

            await message.answer(NEW_DISCUSSION_END_MESSAGE.format(id=problem.get_id()))
            await state.set_data(remove_non_service_data(problem_data))
            await state.reset_state(with_data=False)

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

    if answer == 'Да':
        anonymous_question = True
    elif answer == 'Нет':
        anonymous_question = False
    else:
        await message.answer(NEW_QUESTION_SELECT_YES_OR_NO, reply_markup=kb.get_yes_no_km())
        return

    await state.update_data(anonymous_question=anonymous_question)

    problem = add_new_problem(problem_data['title'], problem_data['body'], message.from_user.id)

    for topic in problem_data['topics']:
        assign_topic(problem, topic[1])

    await message.answer(NEW_QUESTION_END_MESSAGE.format(id=problem.get_id()))
    await state.set_data(remove_non_service_data(problem_data))
    await state.reset_state(with_data=False)


# Question detail
@dp.message_handler(state=QuestionDetailStates.waiting_for_report)
async def handle_report_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    author = message.from_user.id
    problem_id = data.get("problem_id")
    report_body = message.text
    queston_service.report_problem(problem_id=problem_id, report_body=report_body, report_author_id=author)
    # TODO: ADD KB_MARKUP
    await state.set_data(remove_non_service_data(data))
    await message.answer(constants.QUESTION_DETAIL_REPORT_SUBMITTED, reply_markup=kb.ReplyKeyboardRemove())
    # await state.reset_state(with_data=False)
    await QuestionDetailStates.waiting_for_choose_option.set()


@dp.message_handler(state=QuestionDetailStates.waiting_for_problem_id)
async def handle_detail_without_id(message: types.Message, state: FSMContext):
    problem_id = message.text
    problem_obj = queston_service.get_problem_by_id(problem_id)
    if problem_obj is not None:
        message.text = "/detail" + problem_id
        await handle_detail(message, state)


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

    await message.answer(constants.QUESTION_DETAIL_RESPONSE_COMPLETE_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())
    await state.set_data(remove_non_service_data(data))
    message.text = "/detail" + problem_id
    await handle_detail(message, state)


@dp.message_handler(state="*")
async def handle_any_other_message(message: types.Message, state: FSMContext):
    await message.answer("Ошибка! Невозможно выполнить эту команду сейчас!", reply_markup=kb.ReplyKeyboardRemove())
    await send_welcome(message)
