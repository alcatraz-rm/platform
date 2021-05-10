from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationProcessStates(StatesGroup):
    waiting_for_name = State('name')
    waiting_for_email = State('email')
    # waiting_for_interests = State()
    waiting_for_department = State('department')
    waiting_for_degree_level = State('degree_level')


class NewQuestionStates(StatesGroup):
    waiting_for_type = State('type')
    waiting_for_title = State('title')
    waiting_for_body = State('body')
    waiting_for_new_topic_or_quit = State('topic_or_quit')
    waiting_for_anonymous_or_not_answer = State('anonymous')


class InterestsInputStates(StatesGroup):
    waiting_for_science = State('science')
    waiting_for_section = State('section')
    waiting_for_subsection = State('subsection')

