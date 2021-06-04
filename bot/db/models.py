from peewee import *
from .base import BaseModel
from bot import constants
from datetime import datetime


class Science(BaseModel):
    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Science'


class Subject(BaseModel):
    science = ForeignKeyField(Science)

    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name + ' | ' + self.science.name

    class Meta:
        db_table = 'Subject'


class UserModel(BaseModel):
    """
        Fields: name, e-mail, interests, bio, department, degree-level + t_id, t_username.
    """
    t_id = IntegerField()

    t_username = CharField()

    name = CharField()

    email = CharField()

    department = CharField(choices=constants.DEPARTMENT_OPTIONS)

    degree_level = CharField(choices=constants.DEGREE_LEVEL_OPTIONS)

    class Meta:
        db_table = 'User'


class Problem(BaseModel):
    title = CharField()

    body = TextField()

    user = ForeignKeyField(UserModel)

    created_at = DateTimeField(default=datetime.now)

    is_closed = BooleanField(default=False)

    is_anonymous = BooleanField(default=False)

    type = CharField(choices=('question', 'discussion', ))

    invite_link = CharField(default=None, null=True)

    group_id = IntegerField(null=True, default=None)

    class Meta:
        db_table = 'Problem'


class Response(BaseModel):
    problem = ForeignKeyField(Problem, backref='responses')

    body = TextField()

    author = ForeignKeyField(UserModel)

    created_at = DateTimeField(default=datetime.now)

    is_anonymous = BooleanField(default=False)

    is_final = BooleanField(default=False)

    class Meta:
        db_table = 'Response'


class Interest(BaseModel):
    user = ForeignKeyField(UserModel)

    subject = ForeignKeyField(Subject)

    class Meta:
        db_table = 'Interest'


class Topic(BaseModel):
    problem = ForeignKeyField(Problem)

    subject = ForeignKeyField(Subject)

    class Meta:
        db_table = 'Topic'


class ProblemLike(BaseModel):
    problem = ForeignKeyField(Problem)

    liked_by = ForeignKeyField(UserModel)

    class Meta:
        db_table = 'Problem_Like'


class ProblemReport(BaseModel):
    report_problem = ForeignKeyField(Problem)

    author = ForeignKeyField(UserModel)

    report_reason = CharField(choices=constants.REPORT_REASONS_OPTIONS)

    time_stamp = DateTimeField(default=datetime.now)

    is_closed = BooleanField(default=False)

    class Meta:
        db_table = 'Problem_Report'


class UserReport(BaseModel):
    report_user = ForeignKeyField(UserModel)

    author = ForeignKeyField(UserModel)

    report_reason = CharField(choices=constants.REPORT_REASONS_OPTIONS)

    time_stamp = DateTimeField(default=datetime.now)

    is_closed = BooleanField(default=False)

    class Meta:
        db_table = 'User_Report'


class BannedUsers(BaseModel):
    user = ForeignKeyField(UserModel)

    reason = TextField()

    banned_until = DateTimeField()

    is_permanent = BooleanField(default=False)
