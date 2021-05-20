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


question_detail_cb = CallbackData("problem_id", "user_id", "action")


@dp.callback_query_handler(question_detail_cb.filter(action="detail"))
async def handle_detail(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    q_id = callback_data.get("problem_id")
    problem_obj = queston_service.get_problem_by_id(q_id)
    # TODO: add tags to message (via template)
    reply_markup = inline_kb.get_question_detail_inline_kb(problem_obj, call.from_user.id)
    await call.message.answer(problem_obj.body,
                              reply_markup=reply_markup)
    await QuestionDetailStates.waiting_for_choose_option.set()
    await state.update_data(q_id=q_id)


@dp.callback_query_handler(question_detail_cb.filter(action="discussion"))
async def handle_discussion_action(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer("Функция еще недоступна :(.", reply_markup=kb.ReplyKeyboardRemove())
    await call.answer()


@dp.callback_query_handler(question_detail_cb.filter(action=["response"]),
                           state=QuestionDetailStates.response_or_discussion)
async def send_response_form(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    problem_id = callback_data["problem_id"]

    await call.message.answer("Напиши свой ответ в следующем сообщении.", reply_markup=kb.ReplyKeyboardRemove())
    await QuestionDetailStates.waiting_for_response.set()
    await state.update_data(problem_id=problem_id)


@dp.callback_query_handler(question_detail_cb.filter(action=["resp_or_disc"]),
                           state=QuestionDetailStates.waiting_for_choose_option)
async def send_response_or_discussion_poll(call: types.CallbackQuery, callback_data: dict):
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


@dp.callback_query_handler(question_detail_cb.filter(action=["report"]))
async def send_report(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer("Функция еще недоступна :(.", reply_markup=kb.ReplyKeyboardRemove())
    await call.answer()


@dp.callback_query_handler(question_detail_cb.filter(action=["like"]))
async def handle_like(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer("Функция еще недоступна :(.", reply_markup=kb.ReplyKeyboardRemove())
    await call.answer()


@dp.callback_query_handler(text="click")
async def send_random_value(call: types.CallbackQuery):
    """
        DEMO handler
    """
    # Send a message if needed
    await call.message.answer("Click")
    # Finish the callback
    await call.answer(show_alert=False)


