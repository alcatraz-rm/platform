from bot.db.services import queston_service
from bot.config import bot as bot_instance
from aiogram import types


def remove_non_service_data(data: dict):
    """
        Removes all data that are not marked as service.
        :param: data
        :return: only service data (clean data).
        Example:
            instead of using:
                await state.reset_data()
            use:
                await state.set_data(remove_non_service_data(data))
    """
    service_data = {'_time': data['_time']}

    data.clear()
    return service_data


def generate_topic_str(topics: dict, sep="::") -> str:
    topics_str = ""
    for science in topics.keys():
        print(science)
        print(topics[science])
        for t in topics[science]:
            tag = science + sep + t + "; "
            topics_str += tag

    return topics_str


def generate_feed(questions_list):
    questions_str = ''
    question_info_template = '*Заголовок:* {title}\n' \
                             '*ID:* {problem_id}\n' \
                             '*Статус:* {is_open}\n' \
                             '*Подробнее:* /detail{problem_id}\n' \
                             '*Темы:* {topics}'

    for question in questions_list:
        questions_str += '\n\n' + question_info_template.format(title=question.title,
                                                                problem_id=question.id,
                                                                is_open='Закрыт' if question.is_closed else 'Открыт',
                                                                topics=generate_topic_str(
                                                                    queston_service.get_all_topics_for_problem(
                                                                        question.id)))

    return questions_str


async def make_broadcast(message: str, list_of_users: list):
    for user in list_of_users:
        try:
            await bot_instance.send_message(chat_id=user, text=message, parse_mode=types.ParseMode.MARKDOWN)
        except Exception:
            print(f"Can't send message chat_id = {user}")
