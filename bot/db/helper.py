from .base import *
from .models import *


def create_tables():
    try:
        db.connect()
        db.create_tables([UserModel, Science, Subject, Section, ])
    except InternalError as px:
        print(str(px))
