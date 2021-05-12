from peewee import *
from .base import BaseModel
from bot import constants


class UserModel(BaseModel):
    """
        Fields: name, e-mail, interests, bio, department, degree-level + t_id, t_username.
    """
    t_id = IntegerField()

    t_username = CharField()

    name = CharField()

    email = CharField()

    # interests = ForeignKeyField()

    department = CharField(choices=constants.DEPARTMENT_OPTIONS)

    degree_level = CharField(choices=constants.DEGREE_LEVEL_OPTIONS)

    class Meta:
        db_table = 'Users'


class Science(BaseModel):
    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Subject(BaseModel):
    science = ForeignKeyField(Science)

    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name + ' | ' + self.science.name


class Section(BaseModel):
    subject = ForeignKeyField(Subject)

    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name + ' | ' + self.subject.name + ' | ' + self.subject.science.name
