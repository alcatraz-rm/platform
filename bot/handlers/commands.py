from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp, ADMINS_IDS
from bot.db.services.queston_service import get_all_open_questions, add_new_problem, assign_topic

from bot.states import RegistrationProcessStates, NewQuestionStates, AdminPanelStates, InterestsInputStates, \
    SettingsChangeStates, QuestionDetailStates

import bot.keyboards.replay as kb
import bot.keyboards.inline as inline_kb
from bot.db.services import account_service, queston_service
from bot.constants import *
from bot.utils import remove_non_service_data, generate_topic_str

# TODO: add /exit to /new, /settings
# TODO: logging to file
# TODO: fix messages
# TODO: fix register (adding interests)
# TODO: highlight closed question and delete answer button
# TODO: implement interactive report using inline buttons
# TODO: speed up email validation
# TODO: validate degree and department
# TODO: Change /exit from Add interest
# TODO: fix loading department and degree from db in author info
# TODO: add user id validating and alerting
# TODO: handle anonymous question detail
# TODO: resend keyboard markup if error occurred


@dp.message_handler(user_id=ADMINS_IDS,
                    commands=["science", "subject"],
                    state=AdminPanelStates.waiting_for_command)
async def handle_admin_add_interest(message: types.Message, state: FSMContext):
    command = message.text
    if command == '/science':
        await message.answer("Напишите название науки.", reply_markup=kb.ReplyKeyboardRemove())
        await AdminPanelStates.waiting_for_science.set()
    elif command == '/subject':
        await message.answer("Напишите название предмета.", reply_markup=kb.ReplyKeyboardRemove())
        await AdminPanelStates.waiting_for_subject.set()


@dp.message_handler(user_id=ADMINS_IDS, commands=["add"], state=AdminPanelStates.waiting_for_command)
async def handle_admin_add(message: types.Message, state: FSMContext):

    await message.answer("Что добавить? /science, /subject.", reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(commands=["exit"], state=InterestsInputStates.all_states)
async def handle_admin_exit(message: types.Message, state: FSMContext):
    await message.answer("Интересы добавлены.", reply_markup=kb.ReplyKeyboardRemove())
    await state.reset_state(with_data=False)
    await send_welcome(message)


@dp.message_handler(commands=["exit"], state=NewQuestionStates.all_states)
async def handle_new_exit(message: types.Message, state: FSMContext):
    problem_data = await state.get_data()

    if 'type' in problem_data:
        if problem_data['type'] == 'question':
            await message.answer(NEW_EXIT_QUESTION_MESSAGE)
        else:
            await message.answer(NEW_EXIT_DISCUSSION_MESSAGE)

        await state.reset_state(with_data=False)
        await state.set_data(remove_non_service_data(problem_data))

        return

    await message.answer("Создание отменено")
    await state.reset_state(with_data=False)
    await state.set_data(remove_non_service_data(problem_data))


@dp.message_handler(user_id=ADMINS_IDS, commands=["exit"], state=AdminPanelStates.all_states)
async def handle_admin_exit(message: types.Message, state: FSMContext):

    await message.answer("Выход из админки.", reply_markup=kb.ReplyKeyboardRemove())
    await state.reset_state(with_data=False)

    await send_welcome(message)


@dp.message_handler(user_id=ADMINS_IDS, commands=["admin"], state="*")
async def handle_admin(message: types.Message, state: FSMContext):
    await message.answer("Админ команды: /add, /exit.", reply_markup=kb.ReplyKeyboardRemove())
    await AdminPanelStates.waiting_for_command.set()


@dp.message_handler(commands=["exit"], state=SettingsChangeStates.all_states)
async def handle_exit(message: types.Message, state: FSMContext):
    # TODO: remove dat shit!!!
    # TODO: save changes here

    await message.answer("Йоу, бро с настройками покончено. Мне похуй.", reply_markup=kb.ReplyKeyboardRemove())
    await state.set_data(remove_non_service_data(await state.get_data()))
    await state.finish()


@dp.message_handler(commands=["exit"], state=RegistrationProcessStates.all_states)
async def handle_exit(message: types.Message, state: FSMContext):
    await message.answer(constants.REGISTRATION_CANCELED_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())
    await state.set_data(remove_non_service_data(await state.get_data()))
    await state.finish()


@dp.message_handler(commands=["new"], state="*")
async def handle_new(message: types.Message):
    if account_service.is_user_exist(t_id=message.from_user.id):
        await message.answer(NEW_SELECT_TYPE, reply_markup=kb.get_question_type_km())
        await NewQuestionStates.waiting_for_type.set()
    else:
        await message.answer(NEW_REGISTRATION_REQUIRED)


@dp.message_handler(commands=["add", "finish"], state=NewQuestionStates.waiting_for_new_topic_or_quit)
async def handle_add_or_finish(message: types.Message, state: FSMContext):
    command = message.get_command()
    problem_data = await state.get_data()
    type_ = problem_data.get('type')
    answer = ''

    if command == '/add':
        if type_ == 'question':
            answer = NEW_QUESTION_SCIENCE_MESSAGE
        elif type_ == 'discussion':
            answer = NEW_DISCUSSION_SCIENCE_MESSAGE

        await message.answer(answer, reply_markup=kb.get_science_list_km())
        await NewQuestionStates.waiting_for_science.set()

    elif command == '/finish':
        print('finish')
        if type_ == 'discussion':
            await message.answer(NEW_DISCUSSION_THEME_FINISH_MESSAGE)
            # TODO: set type 'discussion'
            problem = add_new_problem(problem_data['title'], problem_data['body'], message.from_user.id, type_=type_)

            for topic in problem_data['topics']:
                assign_topic(problem, topic[1])

        elif type_ == 'question':
            await message.answer(NEW_QUESTION_THEME_FINISH_MESSAGE)
            await message.answer(NEW_QUESTION_ANON_MESSAGE, reply_markup=kb.get_yes_no_km())

            await NewQuestionStates.waiting_for_anonymous_or_not_answer.set()


@dp.message_handler(commands="detail", state="*")
async def handle_detail_without_id(message: types.Message, state: FSMContext):
    answer = "Укажи номер (id) вопроса, по которому хочешь получить информацию."
    await message.answer(answer, reply_markup=kb.ReplyKeyboardRemove())
    await QuestionDetailStates.waiting_for_problem_id.set()


@dp.message_handler(lambda message: message.text.startswith("/detail"), state="*")
async def handle_detail(message: types.Message, state: FSMContext):
    try:
        q_id = int(message.text.replace("/detail", ''))
    except ValueError:
        await message.answer('Некорректный ID вопроса')
        return

    problem_obj = queston_service.get_problem_by_id(q_id)
    if problem_obj is not None:
        is_liked = queston_service.is_problem_liked_by_user(problem_id=q_id, user_t_id=message.from_user.id)
        reply_markup = inline_kb.get_question_detail_inline_kb(problem_obj, message.from_user.id, is_liked=is_liked)
        topics_str = generate_topic_str(queston_service.get_all_topics_for_problem(q_id))
        author_name = problem_obj.user.name if not problem_obj.is_anonymous else "Anonymous"
        answer = constants.QUESTION_DETAIL_MESSAGE.format(id=problem_obj.id,
                                                          title=problem_obj.title,
                                                          author_name=author_name,
                                                          body=problem_obj.body,
                                                          topics=topics_str)
        if is_liked:
            answer += "\n" + constants.QUESTION_DETAIL_LIKED_MESSAGE
        await message.answer(answer, reply_markup=reply_markup, parse_mode=types.ParseMode.MARKDOWN)
        await QuestionDetailStates.waiting_for_choose_option.set()
    else:
        await message.answer("Нет такого вопроса!")
        await handle_feed(message)


@dp.message_handler(commands=["response"], state="*")
async def handle_response_without_id(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(lambda message: message.text.startswith("/response"), state="*")
async def handle_response(message: types.Message, state: FSMContext):
    r_id = int(message.text.replace("/response", ''))
    response_obj = queston_service.get_response_by_id(r_id)
    formatted_date = response_obj.created_at.strftime("%d %b %Y %H:%M:%S")
    answer = constants.QUESTION_DETAIL_RESPONSE_MESSAGE.format(r_id=response_obj.id,
                                                               r_author=response_obj.author.name,
                                                               date=formatted_date,
                                                               body=response_obj.body)
    current_user_id = message.from_user.id
    problem_author_id = response_obj.problem.user.t_id
    reply_markup = inline_kb.get_response_detail_inline_kb(response_obj=response_obj,
                                                           user_id=message.from_user.id,
                                                           is_author=(current_user_id == problem_author_id))

    await message.answer(answer, reply_markup=reply_markup, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands=["register"], state="*")
async def handle_register(message: types.Message):
    """
        This handler will be called when user sends `/register` command
        Check if user is registered.
    """

    if account_service.is_user_exist(t_id=message.from_user.id):
        await message.answer(constants.REGISTRATION_SKIP_MESSAGE)
    else:
        await message.answer(constants.REGISTRATION_START_MESSAGE)
        await message.answer(constants.REGISTRATION_REGISTER_NECESSARY_ONE_MESSAGE +
                             constants.REGISTRATION_EXIT_SENTENCES,
                             reply_markup=kb.ReplyKeyboardRemove())
        await RegistrationProcessStates.waiting_for_name.set()


@dp.message_handler(commands=["me"], state="*")
async def handle_me(message: types.Message):
    user = account_service.get_user(t_id=message.from_user.id)
    if user is not None:
        interest_str = ""
        answer = constants.ME_MET_MESSAGE.format(name=user.name,
                                                 email=user.email,
                                                 interests=interest_str,
                                                 department=user.department,
                                                 degree_level=user.degree_level)
        await message.answer(answer, reply_markup=kb.get_generic_km(['/register']))
    else:
        await message.answer(constants.ME_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(commands=["feed"], state="*")
async def handle_feed(message: types.Message):
    questions = get_all_open_questions()

    questions_str = ''

    for question in questions:
        questions_str += f'{question.id} {question.title}\n'

    await message.answer(questions_str)


@dp.message_handler(commands=["about"], state="*")
async def send_about(message: types.Message):
    """
    This handler will be called when user sends `/about` command
    """

    await message.answer(constants.ABOUT_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(commands=["help"], state="*")
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """

    await message.answer(constants.HELP_MESSAGE, reply_markup=kb.ReplyKeyboardRemove(),
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    user = account_service.get_user(t_id=message.from_user.id)

    if user is not None:
        await message.answer(constants.START_MET_MESSAGE.format(name=user.name), reply_markup=kb.ReplyKeyboardRemove())
        await message.answer(constants.HELP_MESSAGE, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.answer(constants.ABOUT_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())
        await handle_register(message)


@dp.message_handler(commands=["settings"], state="*")
async def handle_settings(message: types.Message):
    user = account_service.is_user_exist(t_id=message.from_user.id)
    if user is None:
        await message.answer(constants.SETTINGS_UNREGISTERED_MESSAGE)
    else:
        await message.answer(constants.SETTINGS_MESSAGE, reply_markup=kb.get_settings_option_km())
        await SettingsChangeStates.waiting_for_option.set()
