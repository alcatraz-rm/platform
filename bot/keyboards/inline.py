from bot.db.services.queston_service import *
from bot.handlers.callbacks import question_detail_cb, response_detail_cb, report_cb


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


def get_response_detail_inline_kb(response_obj: Response, user_id: int, is_author: bool = False):
    response_id = response_obj.id

    report_callback = response_detail_cb.new(response_id=response_id, user_id=user_id, action="report")

    buttons = [
        types.InlineKeyboardButton(text=emoji.emojize("Пожаловаться :warning:"), callback_data=report_callback)
    ]

    if is_author:
        solve_callback = response_detail_cb.new(response_id=response_id, user_id=user_id, action="solve")
        buttons.append(
            types.InlineKeyboardButton(text=emoji.emojize("Помогло :white_check_mark:"), callback_data=solve_callback))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def get_question_detail_inline_kb(problem_obj: Problem, user_id: int, is_liked: bool = False, is_closed: bool = False):
    like_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="like")
    author_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="author_info")
    resp_or_disc_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="resp_or_disc")
    report_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="send_report_keys")

    buttons = []

    if problem_obj.user.t_id != user_id:
        buttons.append(types.InlineKeyboardButton(
            text=emoji.emojize("Отписаться :cross_mark:" if is_liked else "Отслеживать :eyes:",
                               use_aliases=True), callback_data=like_callback))

    buttons.append(types.InlineKeyboardButton(text=emoji.emojize("Автор :copyright:"), callback_data=author_callback))
    buttons.append(
        types.InlineKeyboardButton(text=emoji.emojize("Пожаловаться :warning:"), callback_data=report_callback))

    if problem_obj.type == 'question':
        buttons.append(types.InlineKeyboardButton(text=emoji.emojize("Ответы :speech_balloon:"),
                                                  callback_data=resp_or_disc_callback))
    else:
        buttons.append(types.InlineKeyboardButton(text=emoji.emojize("Перейти к обсуждению :speech_balloon:"),
                                                  url=problem_obj.invite_link))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def get_resp_or_disc_inline_kb(problem_obj: Problem, user_id: int):
    response_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id, action="response")
    others_responses_callback = question_detail_cb.new(problem_id=problem_obj.id, user_id=user_id,
                                                       action="other_responses")

    buttons = [
        types.InlineKeyboardButton(text=emoji.emojize("Ответы других пользователей :mortar_board:"),
                                   callback_data=others_responses_callback),
        types.InlineKeyboardButton(text=emoji.emojize("Написать свой ответ :pencil:"), callback_data=response_callback),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def get_report_options_inline_kb(problem_id: int, user_id: int):
    buttons = []

    for reason in REPORT_REASONS_ALIASES.keys():
        cb = report_cb.new(problem_id=problem_id, user_id=user_id, reason=REPORT_REASONS_ALIASES[reason])
        buttons.append(types.InlineKeyboardButton(text=reason, callback_data=cb))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard
