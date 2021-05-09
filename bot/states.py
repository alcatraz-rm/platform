from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationProcessStates(StatesGroup):
    init_register = State()
    waiting_for_name = State()
    waiting_for_email = State()
    # waiting_for_interests = State()
    waiting_for_department = State()
    waiting_for_degree_level = State()
