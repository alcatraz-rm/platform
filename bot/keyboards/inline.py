from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from bot.constants import DEPARTMENT_OPTIONS, DEGREE_LEVEL_OPTIONS
from bot.db.services.queston_service import *
from bot.handlers.callbacks import question_detail_cb


def get_generic_inline_kb(keyboard_data: dict, row_widths: int = 1):
    """
        Pass a keyboard_data parameter - a dict of [button_text, callback data] pairs.
    """
    buttons = []
    for button_text in keyboard_data:
        buttons.append(types.InlineKeyboardButton(text=button_text,
                                                  callback_data=keyboard_data[button_text]))

    keyboard = types.InlineKeyboardMarkup(row_width=row_widths)
    keyboard.add(*buttons)

    return keyboard


def get_detail_button_inline_kb(problem_id: int, user_id: int):
    """
        Reply markup for message with the question.
        :param problem_id: - problem's id in db
        :param user_id: - user's id in db
    """
    detail_callback = question_detail_cb.new(problem_id=problem_id, user_id=user_id, action="detail")
    detail_button = types.InlineKeyboardButton(text="Подробнее", callback_data=detail_callback)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(detail_button)

    return keyboard


def get_question_detail_inline_kb(problem_obj: Problem, user_id: int):
    like_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="like")
    author_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="author_info")
    resp_or_disc_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="resp_or_disc")
    report_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="report")

    buttons = [
        types.InlineKeyboardButton(text="Лайк", callback_data=like_callback),
        types.InlineKeyboardButton(text="Автор", callback_data=author_callback),
        types.InlineKeyboardButton(text="Пожаловаться", callback_data=report_callback),
        types.InlineKeyboardButton(text="Обсудить или ответить", callback_data=resp_or_disc_callback),
    ]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard


def get_resp_or_disc_inline_kb(problem_obj: Problem, user_id: int):
    discussion_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="discussion")
    response_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="response")

    buttons = [
        types.InlineKeyboardButton(text="Написать ответ", callback_data=response_callback),
        types.InlineKeyboardButton(text="Перейти к обсуждению", callback_data=discussion_callback),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


def get_inline_kb():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(text="Click on me!", callback_data="click"))

    return keyboard
