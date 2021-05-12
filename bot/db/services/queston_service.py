from peewee import DoesNotExist
from datetime import datetime as dt
from bot.db.models import Subject, Science, Problem, Response, Topic, Interest, UserModel


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


def add_new_problem(title: str, body: str, user_t_id: int) -> Problem:
    user = UserModel.get_or_none(t_id=user_t_id)

    new_problem = Problem.create(title=title,
                                 body=body,
                                 user=user,
                                 created_at=dt.now(),
                                 )

    return new_problem


def add_new_response(problem_id: int, body: str, user_t_id: int, is_anonymous: bool):
    user = UserModel.get_or_none(t_id=user_t_id)
    problem_obj = Problem.get_or_none(id=problem_id)

    Response.create(problem=problem_obj,
                    body=body,
                    author=user,
                    created_at=dt.now(),
                    is_anonymous=is_anonymous,
                    )


def assign_interest(user: UserModel, subject: Subject):
    # TODO: must check if there is no None values
    Interest.create(user=user, subject=subject)


def assign_topic(problem: Problem, subject: Subject):
    # TODO: must check if there is no None values
    Topic.create(problem=problem, subject=subject)


def get_all_interests_for_user(user_id: int):
    query = (Subject.select()
             .join(Interest)
             .join(UserModel)
             .where(UserModel.id == user_id))

    return [record.name for record in query]


def get_all_topics_for_problem(problem_id: int):
    query = (Subject.select()
             .join(Interest)
             .join(Problem)
             .where(Problem.id == problem_id))

    return [record.name for record in query]

