from peewee import DoesNotExist

from bot.db.models import UserModel, Interest, Subject

from typing import Optional

# TODO
'''
    def email_validation(self, email: str):
    pass
'''


def add_new_user(t_id, t_username, name, email, department, degree_level):
    UserModel.create(
        t_id=t_id,
        t_username=t_username,
        name=name,
        email=email,
        department=department,
        degree_level=degree_level,
    )


def is_user_exist(t_id) -> bool:
    try:
        UserModel.get(t_id=t_id)
    except DoesNotExist:
        return False

    return True


def get_user(t_id: int) -> Optional[UserModel]:

    return UserModel.get_or_none(t_id=t_id)


def assign_interest(user: UserModel, subject_name: str):
    subject = Subject.get_or_none(name=subject_name)

    user_interests = get_all_interests_for_user(user.t_id)

    if subject_name not in user_interests:
        Interest.create(user=user.id, subject=subject)


def get_all_interests_for_user(user_id: int):
    predicate = (UserModel.t_id == user_id)
    query_interests = ((Interest
                        .select(Interest, UserModel, Subject)
                        .join(UserModel, on=(Interest.user == UserModel.id))
                        .switch(Interest)
                        .join(Subject, on=(Interest.subject == Subject.id))
                        .where(predicate)
                        ))

    return [record.subject.name for record in query_interests]
