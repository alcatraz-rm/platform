# constants

PROBLEM_TYPE_OPTIONS = [
    ('REQUEST', 'Request'),
    ('QUESTION', 'Question'),
]

DEPARTMENT_OPTIONS = [
    ('nsu_mmf', 'Механико-Математический Факультет'),
]

DEGREE_LEVEL_OPTIONS = [
    ('bachelor', 'Бакалавр'),
    ('master', 'Магистр'),
]


# departments aliases, TODO: add full list (in MVP only mmf)
DEPARTMENT_ALIASES = {'Механико-Математический Факультет': 'mmf'}

# degrees aliases, TODO: add full list
DEGREES_ALIASES = {'Бакалавр': 'bachelor', 'Магистр': 'master'}


REPORT_REASONS_OPTIONS = [
    ('Реклама', 'spam'),
    ('offensive_content', 'Оскорбительное содержание'),
    ('wrong_topics', 'Несовпадение тем с содержанием вопроса'),
    ('incorrect_question', 'Некорректный вопрос'),
]


REPORT_REASONS_ALIASES = {
    'Реклама': 'spam',
    'Оскорбительное содержание': 'offensive_content',
    'Несовпадение тем с содержанием вопроса': 'wrong_topics',
    'Некорректный вопрос': 'incorrect_question',
}


# Messages

WELCOME_MESSAGE = """Добро пожаловать. Для подробной информации напишите /help."""

HELP_MESSAGE = """*Доступные команды:*

*1.*\t\t/about - информация о боте

*2.*\t\t/new - создание вопроса или обсуждения 

*3.*\t\t/feed - лента вопросов/обсуждений

*4.*\t\t/detail - детализация вопроса (укажи его id)

*5.*\t\t/me - что я о тебе знаю и видят другие пользователи

*6.*\t\t/my\_questions - твои вопросы

*7.*\t\t/settings - настройки профиля

*8.*\t\t/help - это сообщение
"""

REGISTRATION_EXIT_SENTENCES = "Введите /exit, чтобы прервать регистрацию"

REGISTRATION_CANCELED_MESSAGE = """Регистрация прервана"""

# REGISTRATION_SENTENCES:

REGISTRATION_START_MESSAGE = '''Для начала работы нужно зарегистрироваться'''
REGISTRATION_REGISTER_MET_MESSAGE = """Мы знакомы, теперь мы на Ты. Все команды доступны по /help :)"""
REGISTRATION_REGISTER_NECESSARY_ONE_MESSAGE = """Введите имя"""  # кнопка exit
REGISTRATION_REGISTER_NECESSARY_TWO__MESSAGE = """ Введите корректный адрес студенческой 
электронной почты (доступный только для меня)"""  # кнопка exit
REGISTRATION_REGISTER_SKIP_ONE_MESSAGE = """Выберите, что вам интересно"""  # кнопки skip+интересы
REGISTRATION_REGISTER_SKIP_TWO_MESSAGE = """Выберите свой факультет"""  # кнопки skip+
REGISTRATION_REGISTER_SKIP_THREE_MESSAGE = """Выберите свою степень обучения"""  # кнопки skip+ бакалавр, магистр,
# аспирант
REGISTRATION_SKIP_MESSAGE = """Мы знакомы, теперь мы на Ты. Все команды доступны по /help :)"""
REGISTRATION_EXIT_MESSAGE = """Каежтся, вы не зарегистрированы. Для регистрации используйте /register"""

# START_SENTENCES:


# what can do this bot? 
# кнопка start
ABOUT_MESSAGE = '''Я - бот студентов МЕХМАТА! Нахожу и соединяю людей по учебным вопросам. Создав аккаунт, 
задавай свои вопросы или создавай беседу для совместного обсуждения предмета, а я постараюсь найти ответы и 
заинтересованных людей в том же, что и ты. Список всех команд можно получить через /help'''


START_MESSAGE = """Я помогаю учиться. Создайте свой аккаунт и я найду людей в НГУ, которые попробуют ответить на 
ваши вопросы или захотят вместе с вами
разобрать очередную поточку. Или же вы сами можете кому-то помочь, закрепив свое понимание и получив
опыт объянения. Для начала необходимо создать аккаунт с помощью /register"""
# кнопка register

START_MET_MESSAGE = """С возращением, {name}. Все команды достуны по /help"""

# ME_SENTENCES:


ME_MET_MESSAGE = """Твой профиль:
Имя: {name}
Почта (НГУ): {email}
Интересы: {interests}
Факультет: {department}
Степень обучения: {degree_level}
Твои вопросы: /my_questions
"""

ME_MESSAGE = """ У вас еще нет профиля, нужно зарегистрировться с помощью /register """  # кнопка register

# FEED_SENTENCES:

FEED_MESSAGE = """Выбери, какие вопросы и обсуждения хочешь посмотреть: """  # кнопки all / my interests
FEED_ALL_MESSAGE = """?: {question}, data: {data}, sum of replies: {sum_replies}"""  # кнопка с NUMBER_QUESTION
FEED_MY_INTERESTS_MESSAGE = """?: {question}, {data}, sum of replies: {sum_replies}"""
FEED_NUMBER_QUESTION_MESSAGE = """?: {question},  author: {name}, data: {data}, sum of replies: 
{sum_replies}, 
comments: {replies}"""  # кнопка / detail
# FEED_NUMBER_QUESTION_DETAIL_MESSAGE =  # кнопки: report / reply
FEED_NUMBER_QUESTION_DETAIL_REPORT_MESSAGE = """вопрос отправлен на проверку, спасибо """

# Настройки:

SETTINGS_UNREGISTERED_MESSAGE = """Вы пока что не зарегистрированы. Чтобы зарегистрироваться, отправьте /register"""
SETTINGS_MESSAGE = """Выбери, что хочешь изменить (для выхода из настроек используй /exit):"""  # кнопки имя / факультет / степень обучения / добавить
# интерес / удалить интерес / exit
SETTINGS_EXIT_MESSAGE = """Ты вышел из настроек"""
SETTINGS_NAME_MESSAGE = """Введи новое имя: """  # кнопка exit
SETTINGS_NAME_CHANGED_MESSAGE = """Ты изменил имя на {name}"""
SETTINGS_FACULTY_MESSAGE = """Выбери свой факультет: """  # кнопка exit
SETTINGS_FACULTY_CHANGED_MESSAGE = """Твой факультет изменён на {faculty}"""
SETTINGS_DEGREE_MESSAGE = """Выбери свою степень обучения: """  # кнопка exit
SETTINGS_DEGREE_CHANGED_MESSAGE = """Твоя степень обучения изменена на {degree}"""
SETTINGS_DELETE_MESSAGE = """Выбери интерес, который хочешь удалить:"""  # кнопка exit
SETTINGS_DELETE_FINISH_MESSAGE = """Интерес {interest} удалён"""
SETTINGS_ADD_MESSAGE_1 = """Выбери науку (для возвращения к настройкам используй /finish)"""  # кнопка exit
SETTINGS_ADD_MESSAGE_2 = """Выбери дисциплину (для возвращения к настройкам используй /finish)"""  # кнопка exit / skip
SETTINGS_ADD_FINISH_MESSAGE = """Интерес {interest} добавлен"""
SETTINGS_EXIT_MESSAGE_1 = """Настройка прервана"""

# Создание вопроса / обсуждения:

NEW_SELECT_TYPE = """Выбери тип"""  # кнопка вопрос, обсуждение
NEW_REGISTRATION_REQUIRED = """Зарегистрируйтесь с помощью /register, чтобы создавать вопросы и обсуждения"""
NEW_INCORRECT_TYPE = """Выбери корректный тип, используя клавиатуру"""
NEW_QUESTION_MESSAGE = """Сформулируй название вопроса. Будь конкретен"""  # кнопка exit
NEW_QUESTION_PROBLEM_MESSAGE = """Введи вопрос. Не задавай вопросов, которые допускают спорные или субъективные 
ответы, а также вопросов, которые могут привести к обсуждению (для таких вопросов создай "Обсуждение")"""  # кнопка exit
NEW_QUESTION_THEME_MESSAGE = """Выбери не более 3 тем для совего вопроса"""  # кнопка exit
NEW_QUESTION_SCIENCE_MESSAGE = """Выбери науку"""  # кнопка exit
NEW_QUESTION_DISCIPLINE_MESSAGE = """Выбери дисциплину"""  # кнопка exit / skip
NEW_QUESTION_THEME_SAVED_MESSAGE = """Тема успешно сохранена. Чтобы добавить ещё одну тему, используй кнопку /add. 
Чтобы завершить выбор тем, используй кнопку /finish"""  # кнопки / add / finish / exit
NEW_QUESTION_THEME_FINISH_MESSAGE = """Процесс выбора тем завершён"""  # кнопка exit
NEW_QUESTION_ANON_MESSAGE = """Хочешь задать вопрос анонимно?"""  # кнопки да, нет, exit
NEW_QUESTION_SELECT_YES_OR_NO = """Выбери "Да" или "Нет", используя клавиатуру."""
NEW_QUESTION_END_MESSAGE = """Вопрос сохранён. ID вопроса: {id}"""
NEW_DISCUSSION_MESSAGE = """Сформулируй название обсуждения. Будь конкретен"""  # кнопка exit
NEW_DISCUSSION_PROBLEM_MESSAGE = """Опиши проблему, которую хочешь вынести на обсуждение. Спрашивай о реальной 
проблеме, с которой столкнулся. Подробно опиши, чего хочешь добиться, что уже сделал и что предлагаешь обсудить"""  #
# кнопка exit
NEW_DISCUSSION_THEME_MESSAGE = """Выбери не более 5 тем для обсуждения"""  # кнопка exit
NEW_DISCUSSION_SCIENCE_MESSAGE = """Выбери науку"""  # кнопка exit
NEW_DISCUSSION_DISCIPLINE_MESSAGE = """Выбери дисциплину"""  # кнопка exit / skip
NEW_DISCUSSION_THEME_SAVED_MESSAGE = """Тема успешно сохранена. Чтобы добавить ещё одну тему, используй кнопку /add. 
Чтобы завершить выбор тем, используй кнопку /finish"""  # кнопки / add / finish / exit
NEW_DISCUSSION_THEME_FINISH_MESSAGE = """Процесс выбора тем завершён"""  # кнопка exit
NEW_DISCUSSION_END_MESSAGE = """Обсуждение сохранено. ID обсуждения: {id} """
NEW_EXIT_QUESTION_MESSAGE = """Создание вопроса прервано"""
NEW_EXIT_DISCUSSION_MESSAGE = """Создание обсуждения прервано"""

# Question detail

QUESTION_DETAIL_MESSAGE = """*#{id} {title}*\n\n*Автор:* {author_name}\n\n*Вопрос:* {body}\n\n*Темы:* {topics}\n
Для перехода к ленте вопросов - /feed\nЕсли возникли проблемы - /help"""
DISCUSSION_DETAIL_MESSAGE = """*#{id} {title}*\n\n*Автор:* {author_name}\n\n*Проблема:* {body}\n\n*Темы:* {topics}\n
Для перехода к ленте вопросов - /feed\nЕсли возникли проблемы - /help"""

QUESTION_DETAIL_LIKED_MESSAGE = """_Ты отслеживаешь этот вопрос._"""
QUESTION_DETAIL_LIKED_ALERT = "Теперь ты отслеживаешь этот вопрос"
QUESTION_DETAIL_DISLIKED_ALERT = "Ты убрал лайк. Ты больше не отслеживаешь этот вопрос"
QUESTION_DETAIL_AUTHOR_INFO = """*Информация об авторе:*
:white_small_square:*Имя:* {name}
:white_small_square:*Интересы:* {interests}
:white_small_square:*Факультет:* {department}
:white_small_square:*Степень обучения:* {degree_level}
"""
QUESTION_DETAIL_REPORT_INIT = "Выбери причину жалобы"
QUESTION_DETAIL_REPORT_SUBMITTED = "Спасибо за жалобу. Мы рассмотрим ее в кратчайшие сроки и примем взвешанное решение"
QUESTION_DETAIL_CALLBACK_ERROR_ALERT = """Ошибка! Это действие уже нельзя выполнить. 
Выполните команду /detail%id%, где вместо %id% укажите id впороса, который вас интересует"""
QUESTION_DETAIL_CALLBACK_ERROR_MESSAGE = """Для перехода к ленте вопросов - /feed\nЕсли возникли проблемы - /help"""
QUESTION_DETAIL_RESPONSE_COMPLETE_MESSAGE = """Спасибо за ответ! Автор вопроса скоро получит уведомление"""
QUESTION_DETAIL_RESPONSE_FEED_TEMPLATE = """*Ответ от пользователя {r_author} от {date}:*\n{small_body}...
_Посмотреть подробности /response{p_id}._\n\n"""
QUESTION_DETAIL_RESPONSE_MESSAGE = """*#{r_id} Ответ от пользователя {r_author} от {date}:*\n\n*Ответ:* {body}\n\n
Для перехода к ленте вопросов - /feed\nЕсли возникли проблемы - /help"""

QUESTION_DETAIL_UPDATE_NOTIFICATION = """*Новое уведомление: кто-то ответил на вопрос, который ты отслеживаешь*\n
*Название вопроса:* {title}\n
*Вопрос:* /detail{problem_id}\n
_Для просмотра напиши /response{response_id}_"""
QUESTION_DETAIL_CLOSED_NOTIFICATION_MESSAGE = """*Новое уведомление: твой ответ помог автору*\n
*Название вопроса:* {title}\n
*Вопрос:* /detail{problem_id}\n
*Ответ:* /response{response_id}\n
*Спасибо!*"""
QUESTION_DETAIL_UPDATE_NOTIFICATION_FOR_AUTHOR = """*Новое уведомление: на твой вопрос ответили*\n
*Название вопроса:* {title}\n
*Вопрос:* /detail{problem_id}\n
_Для просмотра напиши /response{response_id}_"""

