from peewee import *
from playhouse.migrate import *

from bot.config import DATABASE_PASSWORD, DATABASE_NAME, DATABASE_HOST, DATABASE_USER, DATABASE_PORT


db = PostgresqlDatabase(
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT
)

migrator = PostgresqlMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db
