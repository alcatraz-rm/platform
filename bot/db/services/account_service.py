from peewee import DoesNotExist, InternalError

from bot.constants import DEPARTMENT_ALIASES, DEGREES_ALIASES
from bot.db.models import UserModel, Interest, Subject, BannedUsers

from typing import Optional
from email_validator import validate_email, EmailNotValidError
from bot.config import bot as bot_instance
from datetime import datetime


def email_is_valid(email: str):
    if '@g.nsu.ru' not in email:
        return False

    try:
        validate_email(email)
    except EmailNotValidError:
        return False

    return True


def add_new_user(t_id, t_username, name, email, department, degree_level):
    try:
        UserModel.create(
            t_id=t_id,
            t_username=t_username,
            name=name,
            email=email,
            department=DEPARTMENT_ALIASES[department],
            degree_level=DEGREES_ALIASES[degree_level],
        )
    except InternalError:
        UserModel.create(
            t_id=t_id,
            t_username=t_username,
            name=name,
            email=email,
            department=DEPARTMENT_ALIASES[department],
            degree_level=DEGREES_ALIASES[degree_level],
        )


def is_user_exist(t_id) -> bool:
    try:
        UserModel.get(t_id=t_id)
    except DoesNotExist:
        return False

    return True


def get_user(t_id: int) -> Optional[UserModel]:
    try:
        user = UserModel.get_or_none(t_id=t_id)
    except InternalError:
        user = UserModel.get_or_none(t_id=t_id)

    if user:
        user.department = {value: key for key, value in DEPARTMENT_ALIASES.items()}[user.department]
        user.degree_level = {value: key for key, value in DEGREES_ALIASES.items()}[user.degree_level]

    return user


def assign_interest(user: UserModel, subject_name: str):
    subject = Subject.get_or_none(name=subject_name)
    user_interests = get_all_interests_for_user(user.t_id)

    if subject.science.name not in user_interests.keys():
        try:
            Interest.create(user=user.id, subject=subject)
            return
        except InternalError:
            Interest.create(user=user.id, subject=subject)
            return

    if subject_name not in user_interests.get(subject.science.name):
        try:
            Interest.create(user=user.id, subject=subject)
        except InternalError:
            Interest.create(user=user.id, subject=subject)


def remove_interest(user: UserModel, subject_name: str):
    """
        Removes interest for user. If subject with given name wasn't found DoesNotExist exception is being thrown.
    """
    subject = Subject.get_or_none(name=subject_name)
    if subject is not None:
        interest = Interest.get_or_none(user=user, subject=subject)

        if interest is not None:
            Interest.delete_by_id(interest.id)
        else:
            raise DoesNotExist("User {} doesn't have given interest \"{}\".".format(user.t_username, subject.name))
    else:
        raise DoesNotExist("Subject \"{}\" doesn't exist.".format(subject_name))


def get_all_interests_for_user(user_id: int) -> dict:
    """
        Returns a dict of pairs {subject_name, science_name (linked to the subject)}.
    """
    predicate = (UserModel.t_id == user_id)
    query_interests = ((Interest
                        .select(Interest, UserModel, Subject)
                        .join(UserModel, on=(Interest.user == UserModel.id))
                        .switch(Interest)
                        .join(Subject, on=(Interest.subject == Subject.id))
                        .where(predicate)
                        ))
    subjects = {}
    for record in query_interests:
        if subjects.__contains__(record.subject.science.name):
            subjects[record.subject.science.name].append(record.subject.name)
        else:
            subjects[record.subject.science.name] = [record.subject.name]

    return subjects


def alter_user_info(user: UserModel, name: str = None, email: str = None,
                    department: str = None, degree_level: str = None):
    user.department = DEPARTMENT_ALIASES[user.department]
    user.degree_level = DEGREES_ALIASES[user.degree_level]

    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if department is not None:
        user.department = DEPARTMENT_ALIASES[department]
    if degree_level is not None:
        user.degree_level = DEGREES_ALIASES[degree_level]

    try:
        user.save()
    except InternalError:
        user.save()


async def ban_user(user_id: int, reason: str, banned_until: datetime, is_permanent: bool = False):
    user = UserModel.get_or_none(id=user_id)
    try:
        BannedUsers.create(user=user,
                           reason=reason,
                           banned_until=banned_until,
                           is_permanent=is_permanent)
    except InternalError:
        BannedUsers.create(user=user,
                           reason=reason,
                           banned_until=banned_until,
                           is_permanent=is_permanent)

    mes = f"Ваш аккаунт был заблокирован.\n\nПричина: {reason}"
    await bot_instance.send_message(chat_id=user.t_id, text=mes)
