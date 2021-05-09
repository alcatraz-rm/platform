from peewee import DoesNotExist

from bot.db.models import UserModel

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
