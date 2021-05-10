from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from bot.constants import DEPARTMENT_OPTIONS, DEGREE_LEVEL_OPTIONS


def get_department_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for dep in DEPARTMENT_OPTIONS:
        keyboard.add(dep[1])

    return keyboard


def get_degree_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for dep in DEGREE_LEVEL_OPTIONS:
        keyboard.add(dep[1])

    return keyboard
