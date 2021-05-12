from .base import *
from .models import *


def create_tables():
    try:
        db.connect()
        db.create_tables([UserModel, Science, Subject, Problem, Response, Interest])
    except InternalError as px:
        print(str(px))


def migrate_db():
    """
        If you need to migrate, type here all changes you you have made
         and then run it in python shell before running a server.
    """
    field = ForeignKeyField(Interest, backref='Users')
    migrate(
        migrator.add_column('Users', 'interests', field),
        # migrator.add_not_null('User', 'interests', field),
        # migrator.add_foreign_key_constraint('Users', 'interests', field)
    )

