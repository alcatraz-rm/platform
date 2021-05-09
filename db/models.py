from peewee import *
from .db_config import dbhandle


class BaseModel(Model):
    id = PrimaryKeyField(null=False)

    class Meta:
        database = dbhandle

# TODO make db models for auth and question apps.
