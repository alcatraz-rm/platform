from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp, ADMINS_IDS

from bot.states import RegistrationProcessStates, NewQuestionStates, AdminPanelStates, InterestsInputStates, \
    SettingsChangeStates, QuestionDetailStates

import bot.keyboards.replay as kb
import bot.keyboards.inline as inline_kb
from bot.db.services import account_service, queston_service
from bot.constants import *
from bot.utils import remove_non_service_data, generate_topic_str


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


@dp.message_handler(user_id=ADMINS_IDS, commands=["exit"], state=AdminPanelStates.all_states)
async def handle_admin_exit(message: types.Message, state: FSMContext):

    await message.answer("Выход из админки.", reply_markup=kb.ReplyKeyboardRemove())
    await state.reset_state(with_data=False)

    await send_welcome(message)


@dp.message_handler(user_id=ADMINS_IDS, commands=["admin"], state="*")
async def handle_admin(message: types.Message, state: FSMContext):
    await message.answer("Админ команды: /add, /exit.", reply_markup=kb.ReplyKeyboardRemove())
    await AdminPanelStates.waiting_for_command.set()


@dp.message_handler(commands=["interests"], state="*")
async def handle_interest(message: types.Message, state: FSMContext):
    await message.answer("Выберите интересную вам науку.", reply_markup=kb.get_science_list_km())
    await InterestsInputStates.waiting_for_science.set()


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
async def handle_new(message: types.Message, state: FSMContext):
    command = message.get_command()
    problem_data = await state.get_data()
    type_ = problem_data.get('type')
    answer = ''

    if command == 'add':
        if type_ == 'question':
            answer = NEW_QUESTION_DISCIPLINE_MESSAGE
        elif type_ == 'discussion':
            answer = NEW_DISCUSSION_DISCIPLINE_MESSAGE

        await message.answer(answer, reply_markup=kb.get_science_list_km())
        await InterestsInputStates.waiting_for_science.set()

    elif command == 'finish':
        if type_ == 'discussion':
            await message.answer(NEW_DISCUSSION_THEME_FINISH_MESSAGE)
        elif type_ == 'question':
            await message.answer(NEW_QUESTION_THEME_FINISH_MESSAGE)
            await message.answer(NEW_QUESTION_ANON_MESSAGE, reply_markup=kb.get_yes_no_km())

            await NewQuestionStates.waiting_for_anonymous_or_not_answer.set()


@dp.message_handler(lambda message: message.text.startswith("/detail"), state="*")
async def handle_detail(message: types.Message, state: FSMContext):
    q_id = int(message.text.replace("/detail", ''))
    problem_obj = queston_service.get_problem_by_id(q_id)
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
    if user is None:
        await message.answer(constants.ME_MESSAGE + "/register")
    else:
        await message.answer(constants.ME_MET_MESSAGE)


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

    await message.answer(constants.HELP_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    user = account_service.get_user(t_id=message.from_user.id)

    if user is not None:
        await message.answer(constants.START_MET_MESSAGE.format(name=user.name), reply_markup=kb.ReplyKeyboardRemove())
        await message.answer(constants.HELP_MESSAGE)
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
