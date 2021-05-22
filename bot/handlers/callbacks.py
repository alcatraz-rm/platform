from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp, ADMINS_IDS
from bot.states import RegistrationProcessStates, NewQuestionStates, AdminPanelStates, InterestsInputStates, QuestionDetailStates
from bot.db.services import account_service, queston_service
from bot.constants import *
from bot.utils import remove_non_service_data
from aiogram.utils.callback_data import CallbackData
import bot.keyboards.inline as inline_kb
import bot.keyboards.replay as kb
from bot.utils import remove_non_service_data, generate_topic_str
import emoji

# user_id is telegram_id
question_detail_cb = CallbackData("problem", "problem_id", "user_id", "action")
response_detail_cb = CallbackData("response", "response_id", "user_id", "action")


@dp.callback_query_handler(question_detail_cb.filter(action="discussion"))
async def handle_discussion_action(call: types.CallbackQuery, callback_data: dict):
    await call.answer("Функция еще недоступна :(", show_alert=True)


@dp.callback_query_handler(question_detail_cb.filter(action=["response"]),
                           state=QuestionDetailStates.response_or_discussion)
async def send_response_form(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    problem_id = callback_data["problem_id"]

    await call.message.answer("Напиши свой ответ в следующем сообщении.", reply_markup=kb.ReplyKeyboardRemove())
    await QuestionDetailStates.waiting_for_response.set()
    await state.update_data(problem_id=problem_id)
    await call.answer()


@dp.callback_query_handler(question_detail_cb.filter(action=["resp_or_disc"]),
                           state=QuestionDetailStates.waiting_for_choose_option)
async def send_response_or_discussion_poll(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
        Asks if user want to make a response for question or go to a discussion group-chat.
        Returns a message with two inline buttons.
    """
    user_id = callback_data["user_id"]
    problem_id = callback_data["problem_id"]
    problem_obj = queston_service.get_problem_by_id(problem_id)
    await call.message.answer("Обсудить или ответить?",
                              reply_markup=inline_kb.get_resp_or_disc_inline_kb(problem_obj, user_id))
    await call.answer()
    await QuestionDetailStates.response_or_discussion.set()


@dp.callback_query_handler(question_detail_cb.filter(action=["author_info"]),
                           state=QuestionDetailStates.waiting_for_choose_option)
async def send_author_info(call: types.CallbackQuery, callback_data: dict):
    author = queston_service.get_problem_by_id(callback_data["problem_id"]).user

    interests_str = generate_topic_str(account_service.get_all_interests_for_user(author.t_id))

    answer = constants.QUESTION_DETAIL_AUTHOR_INFO.format(name=author.name,
                                                          interests=interests_str,
                                                          department=author.department,
                                                          degree_level=author.degree_level)

    await call.message.answer(emoji.emojize(answer),
                              reply_markup=kb.ReplyKeyboardRemove(),
                              parse_mode=types.ParseMode.MARKDOWN)
    await call.answer()


@dp.callback_query_handler(question_detail_cb.filter(action=["report"]),
                           state=QuestionDetailStates.waiting_for_choose_option)
async def send_report(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(constants.QUESTION_DETAIL_REPORT_INIT, reply_markup=kb.ReplyKeyboardRemove())
    await call.answer()
    await QuestionDetailStates.waiting_for_report.set()
    await state.update_data(problem_id=callback_data["problem_id"])


@dp.callback_query_handler(question_detail_cb.filter(action=["like"]),
                           state=QuestionDetailStates.waiting_for_choose_option)
async def handle_like(call: types.CallbackQuery, callback_data: dict):
    user_t_id = int(callback_data["user_id"])
    problem_id = callback_data["problem_id"]

    problem_obj = queston_service.get_problem_by_id(problem_id)

    topics_str = generate_topic_str(queston_service.get_all_topics_for_problem(problem_id))
    author_name = problem_obj.user.name if not problem_obj.is_anonymous else "Anonymous"
    answer = constants.QUESTION_DETAIL_MESSAGE.format(id=problem_obj.id,
                                                      title=problem_obj.title,
                                                      author_name=author_name,
                                                      body=problem_obj.body,
                                                      topics=topics_str)
    if queston_service.is_problem_liked_by_user(problem_id=problem_id, user_t_id=user_t_id):
        # dislike
        reply_markup = inline_kb.get_question_detail_inline_kb(problem_obj, call.from_user.id, is_liked=False)
        queston_service.dislike_problem(problem_id=problem_id, user_t_id=user_t_id)
        await call.message.edit_text(answer, reply_markup=reply_markup, parse_mode=types.ParseMode.MARKDOWN)
        await call.answer(constants.QUESTION_DETAIL_DISLIKED_ALERT, show_alert=True)
    else:
        # like
        queston_service.like_problem(problem_id=problem_id, user_t_id=user_t_id)
        reply_markup = inline_kb.get_question_detail_inline_kb(problem_obj, call.from_user.id, is_liked=True)
        answer += "\n" + constants.QUESTION_DETAIL_LIKED_MESSAGE

        await call.message.edit_text(answer, reply_markup=reply_markup, parse_mode=types.ParseMode.MARKDOWN)
        await call.answer(constants.QUESTION_DETAIL_LIKED_ALERT, show_alert=True)


@dp.callback_query_handler(question_detail_cb.filter(action=["other_responses"]),
                           state=QuestionDetailStates.response_or_discussion)
async def handle_other_users_responses(call: types.CallbackQuery, callback_data: dict):
    problem_id = callback_data["problem_id"]
    responses = queston_service.get_all_responses_for_problem(problem_id=problem_id)
    resp_temp = constants.QUESTION_DETAIL_RESPONSE_FEED_TEMPLATE
    answer = "Ответы от пользователей:\n\n"
    for res in responses:
        sb = res.body[:32] if len(res.body) > 32 else res.body
        formatted_date = res.created_at.strftime("%d %b %Y %H:%M:%S")

        t = resp_temp.format(r_author=res.author.name,
                             date=formatted_date,
                             small_body=sb,
                             p_id=res.id)
        answer += t
    await call.message.answer(answer, parse_mode=types.ParseMode.MARKDOWN)
    await call.answer()


@dp.callback_query_handler(response_detail_cb.filter(action="report"), state="*")
async def handle_report_response(call: types.CallbackQuery, callback_data: dict):
    await call.answer("Функция еще недоступна :(", show_alert=True)


@dp.callback_query_handler(response_detail_cb.filter(action="solve"), state="*")
async def resolve_problem(call: types.CallbackQuery, callback_data: dict):
    response_id = callback_data["response_id"]
    queston_service.close_problem_via_response(response_id)
    await call.answer("Ты закрыл впорос.", show_alert=True)


@dp.callback_query_handler(question_detail_cb.filter(), state="*")
async def handle_anything_else(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer(constants.QUESTION_DETAIL_CALLBACK_ERROR_MESSAGE, reply_markup=kb.ReplyKeyboardRemove())
    await call.answer(constants.QUESTION_DETAIL_CALLBACK_ERROR_ALERT, show_alert=True)
