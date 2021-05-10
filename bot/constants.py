# constants

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


REGISTRATION_SENTENCES:


  REGISTRATION_REGISTER_MESSAGE = """Мы знакомы, теперь мы на Ты. Все команды доступны по /help :)""" 
  REGISTRATION_REGISTER_MESSAGE = """ Введите Имя """ //кнопка exit//, """ Введите корректный адрес студенческой электронной почты (доступный только для меня)""" //кнопка exit//, """Выберите что вам интересно""" //кнопки skip+интересы//,
"""Выберите свой факультет"""//кнопки skip+// , """Выберите свою степень обучения""" //кнопки skip+бакалавр, магистр, аспирант//

  REGISTRATION_SKIP_MESSAGE = """Мы знакомы, теперь мы на Ты. Все команды доступны по /help :)"""
  REGISTRATION_EXIT_MESSAGE = """Неавторизованный пользователь. Для регистрации пишите /register."""


START_SENTENCES:

    what can do this bot? //кнопка start//
Я - бот студентов МЕХМАТА! Нахожу и соединяю людей по учебным вопросам. Создав аккаунт, задавай свои вопросы или 
создавай беседу для обсуждения предмета/совместного ботанья, а я постараюсь найти ответы и заинтересованных людей в том же, что и ты. 

   START_MESSAGE = """Йоу, Я помогаю учиться. Создайте свой аккаунт и Я найду людей в НГУ, которые попробуют ответить на ваши truescience вопросы или захотят вместе с вами
  заботать очередную поточку. Или же Вы сами можете кому-то помочь развеять непонимание, закрепив свое понимание и получив опыт объянения. Для начала необходимо создать аккаунт"""
  //кнопка register//

   START_MESSAGE = """йоу, с возращением, бро {{ name }}. Все команды достуны по /help"""


ME_SENTENCES:
     
        
    ME_MESSAGE = """Твой профиль:
    Имя: {{ name }}
    Почта(НГУ).вижутолькоЯ:{{ address }}
    Интересы: {{ interests }}
    Факультет: {{ department}}
    Степень обучения: {{ degree level }}
    """

    ME_MESSAGE = """ Создайте аккаунт моментально. """ //кнопка register//
    
    
FEED_SENTENCES:
    
    
    FEED_MESSAGE = """Выбери, какие вопросы и обсуждения хочешь посмотреть: """ //кнопки all, my interests// 
    FEED_ALL_MESSAGE = """?: {{question}}, data: {{data}}, sum of replies: {{sum_replies}}""" //кнопка с NUMBER_QUESTION //
    FEED_MY_INTERESTS_MESSAGE = """?: {{question}}, {{data}}, sum of replies: {{sum_replies}}"""
    FEED_NUMBER_QUESTION_MESSAGE = """?: {{question}},  author: {{name}}, data: {{data}}, sum of replies: {{sum_replies}}, comments: {{replies}}""" //кнопка /detail //
    FEED_NUMBER_QUESTION_DETAIL_MESSAGE =  //кнопки: /report, /reply / //
    FEED_NUMBER_QUESTION_DETAIL_REPORT_MESSAGE = """вопрос отправлен на проверку, спасибо """
    
    
    
    
    
