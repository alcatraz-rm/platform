from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationProcessStates(StatesGroup):
    waiting_for_name = State('name')
    waiting_for_email = State('email')
    # waiting_for_interests = State()
    waiting_for_department = State('department')
    waiting_for_degree_level = State('degree_level')
