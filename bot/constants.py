#constants

PROBLEM_TYPE_OPTIONS = [
    ('REQUEST', 'Request'),
    ('QUESTION', 'Question'),
]

DEPARTMENT_OPTIONS = [
    ('nsu_mmf', 'Механико Математический Факультет'),
    ('nsu_gi', 'Гуманитарный институт'),
]

DEGREE_LEVEL_OPTIONS = [
    ('bachelor', 'Бакалавр'),
    ('master', 'Магистр'),
]

# Messages

WELCOME_MESSAGE = """Добро пожаловать. Для подробной информации напишите /help."""

HELP_MESSAGE = """Доступные команды:

1. /start - включение бота

2. /help - описание доступных команд

3. /register - регистрация

4. /feed - выводит ленту вопросов или обсуждения

5. /me - что я о тебе знаю и видят другие пользователи 

6. /settings - редактирование профиля 

7. /detail - детализация вопроса (укажи его id)

8. /new - создание обсуждения (/discussion) или вопроса (/question)

9. /user - немного информации о товарище (укажи его id/имя)"""


REGISTRATION_EXIT_SENTENCES = " Type /exit to cancel registration."

REGISTRATION_CANCELED_MESSAGE = """Знакомство не удалось... Захочешь вернуться к этому, пиши /register."""

'''
# REGISTRATION_SENTENCES:


REGISTRATION_REGISTER_MET_MESSAGE = """Мы знакомы, теперь мы на Ты. Все команды доступны по /help :)""" 
REGISTRATION_REGISTER_NECESSARY_ONE_MESSAGE = """ Введите Имя """ #кнопка exit#
REGISTRATION_REGISTER_NECESSARY_TWO__MESSAGE = """ Введите корректный адрес студенческой 
электронной почты (доступный только для меня)""" #кнопка exit#
REGISTRATION_REGISTER_SKIP_ONE_MESSAGE = """Выберите что вам интересно""" #кнопки skip+интересы#
REGISTRATION_REGISTER_SKIP_TWO_MESSAGE = """Выберите свой факультет"""#кнопки skip+#
REGISTRATION_REGISTER_SKIP_THREE_MESSAGE = """Выберите свою степень обучения""" #кнопки skip+бакалавр, магистр, аспирант#
REGISTRATION_SKIP_MESSAGE = """Мы знакомы, теперь мы на Ты. Все команды доступны по /help :)"""
REGISTRATION_EXIT_MESSAGE = """Неавторизованный пользователь. Для регистрации пишите /register."""


# START_SENTENCES:


    # what can do this bot? #кнопка start#
Я - бот студентов МЕХМАТА! Нахожу и соединяю людей по учебным вопросам. Создав аккаунт, задавай свои вопросы или 
создавай беседу для обсуждения предмета/совместного ботанья, а я постараюсь найти ответы и заинтересованных людей в том
 же, что и ты.#

START_MESSAGE = """Йоу, Я помогаю учиться. Создайте свой аккаунт и Я найду людей в НГУ, которые попробуют ответить на 
   ваши truescience вопросы или захотят вместе с вами
  заботать очередную поточку. Или же Вы сами можете кому-то помочь развеять непонимание, закрепив свое понимание и получив
   опыт объянения. Для начала необходимо создать аккаунт"""
  #кнопка register#

START_MET_MESSAGE = """йоу, с возращением, бро {{ name }}. Все команды достуны по /help"""


# ME_SENTENCES:
     
        
    ME_MET_MESSAGE = """Твой профиль:
    Имя: {{ name }}
    Почта(НГУ).вижутолькоЯ:{{ address }}
    Интересы: {{ interests }}
    Факультет: {{ department}}
    Степень обучения: {{ degree level }}
    """

    ME_MESSAGE = """ Создайте аккаунт моментально. """ #кнопка register#
    
    
# FEED_SENTENCES:
    
    
    FEED_MESSAGE = """Выбери, какие вопросы и обсуждения хочешь посмотреть: """ #кнопки all, my interests#
    FEED_ALL_MESSAGE = """?: {{question}}, data: {{data}}, sum of replies: {{sum_replies}}""" #кнопка с NUMBER_QUESTION#
    FEED_MY_INTERESTS_MESSAGE = """?: {{question}}, {{data}}, sum of replies: {{sum_replies}}"""
    FEED_NUMBER_QUESTION_MESSAGE = """?: {{question}},  author: {{name}}, data: {{data}}, sum of replies: 
    {{sum_replies}}, 
    comments: {{replies}}""" #кнопка /detail #
    FEED_NUMBER_QUESTION_DETAIL_MESSAGE =  #кнопки: /report, /reply / #
    FEED_NUMBER_QUESTION_DETAIL_REPORT_MESSAGE = """вопрос отправлен на проверку, спасибо """
    
   
# SETTINGS_SENTENCES:
    
    
    SETTINGS_UNREGISTERED_MESSAGE = """Ты пока что не зарегистрирова, чтобы зарегистрироваться, отправь /register"""
    SETTINGS_MESSAGE = """Выбери, что хочешь изменить: """ #кнопки имя, био, факультет, степень обучения, добавить интерес, удалить интерес, exit# 
    SETTINGS_EXIT_MESSAGE = """Ты вышел из настроек"""
    SETTINGS_NAME_MESSAGE = """Введи новое имя: """ #кнопка exit# """Ты изменил имя на {{name}}""" 
    SETTINGS_BIO_MESSAGE = """Введи новое био: """ #кнопка exit# """Твой био изменён""" 
    SETTINGS_FACULTY_MESSAGE = """Введи свой факультет: """ #кнопка exit# """Твой факультет изменён на {{faculty}}""" 
    SETTINGS_DEGREE_MESSAGE = """Введи свою степень обучения: """ #кнопка exit# """Твоя степень обучения изменена на 
    {{degree}}""" 
    SETTINGS_DELETE_MESSAGE = """Выбери интерес, который хочешь удалить: {{list of interests}}"""#кнопка exit
    # """Интерес {{interest}} удалён"""
    SETTINGS_ADD_MESSAGE = """Выбери науку {{list of sciences}}""" #кнопка exit#
     """Выбери дисциплину 
    {{list of disciplines}}""" 
    #кнопка exit, skip# """Выбери раздел {{list of sections}}""" #кнопка exit, skip# """Интерес {{interest}} добавлен"""
    SETTINGS_EXIT_MESSAGE = """Настройка прервана"""

    
# NEW_SENTENCES:
    
    
    NEW_QUESTION_MESSAGE = """Сформулируй название вопроса. Будь конкретен""" #кнопка exit# """Введи вопрос.
     Не задавай вопросов, которые допускают спорные или субъективные ответы, а также вопросов, которые могут привести к
      обсуждению (для таких вопросов создай обуждение)""" #кнопка exit#
"""Выбери не более 3 тем для совего вопроса""" #кнопка exit# """Выбери науку {{list of sciences}}""" #кнопка exit#
"""Выбери дисциплину {{list of disciplines}}""" #кнопка exit, skip# """Выбери раздел {{list of sections}}""" 
#кнопка exit, skip# 
"""Тема успешно сохранена. Чтобы добавить ещё одну тему, используй кнопку /add. Чтобы завершить выбор тем, 
используй кнопку /finish""" #кнопки , add, finish, exit# """Процесс выбора тем завершён""" #кнопка exit#
  """Хочешь задать вопрос анонимно?""" #кнопки да, нет, exit#
"""Вопрос сохранён и отправлен на модерацию. По итогам проверки тебе придёт сообщение с результатом. ID вопроса: {{id}}
"""
    NEW_DISCUSSION_MESSAGE = """Сформулируй название обсуждения. Будь конкретен""" #кнопка exit#
     """Опиши проблему, которую хочешь вынести на обсуждение. Спрашивай о реальной проблеме, с которой столкнулся. 
     Подробно опиши, чего хочешь добиться, что уже сделал и что предлагаешь обсудить""" #кнопка exit# 
"""Выбери не более 5 тем для совего вопроса""" #кнопка exit# """Выбери науку {{list of sciences}}""" #кнопка exit# 
"""Выбери дисциплину {{list of disciplines}}""" #кнопка exit, skip# """Выбери раздел {{list of sections}}"""
 #кнопка exit, skip#
"""Тема успешно сохранена. Чтобы добавить ещё одну тему, используй кнопку /add. Чтобы завершить выбор тем, 
используй кнопку /finish""" #кнопки , add, finish, exit# """Процесс выбора тем завершён""" #кнопка exit#
"""Обсуждение сохранёно и отправлено на модерацию. По итогам проверки тебе придёт сообщение с результатом. 
ID обсуждения: {{id}}"""
    NEW_EXIT_MESSAGE = """Cоздание {{вопроса/обсуждения}} отменено"""
'''
