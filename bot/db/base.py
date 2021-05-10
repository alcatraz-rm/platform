from peewee import *

from bot.config import DATABASE_PASSWORD, DATABASE_NAME, DATABASE_HOST, DATABASE_USER


db = PostgresqlDatabase(
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
)


class BaseModel(Model):
    class Meta:
        database = db
