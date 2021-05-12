from peewee import DoesNotExist

from bot.db.models import Subject, Science


def add_new_science(name: str):
    Science.create(name=name)


def add_new_subject(name: str, science_name: str):
    science_obj = Science.get_or_none(name=science_name)
    if science_obj is not None:
        Subject.create(name=name, science=science_obj)
    else:
        raise DoesNotExist("Science with name {} doesn't exist.".format(science_name))


def get_all_sciences():
    query = Science.select()
    sciences = [record.name for record in query]

    return sciences


def get_all_subjects(science_name: str):
    query = Subject.select().join(Science).where(Science.name == science_name)
    subjects = [record.name for record in query]

    return subjects

