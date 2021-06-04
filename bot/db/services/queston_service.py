import typing
from datetime import datetime as dt

from aiogram import types
from peewee import DoesNotExist, InternalError

from bot.config import bot as bot_instance
from bot.constants import *
from bot.constants import REPORT_REASONS_ALIASES
from bot.db.models import Subject, Science, Problem, Response, Topic, UserModel, ProblemLike, ProblemReport
from bot.utils import make_broadcast


def add_new_science(name: str):
    try:
        Science.create(name=name)
    except InternalError:
        Science.create(name=name)


def add_new_subject(name: str, science_name: str):
    science_obj = Science.get_or_none(name=science_name)

    if science_obj is not None:
        try:
            Subject.create(name=name, science=science_obj)
        except InternalError:
            Subject.create(name=name, science=science_obj)
    else:
        raise DoesNotExist("Science with name {} doesn't exist.".format(science_name))


def get_all_sciences():
    query = Science.select()
    sciences = [record.name for record in query]

    return sciences


def get_all_subjects(science_name: str):
    query = (Subject.select()
             .join(Science)
             .where(Science.name == science_name))
    subjects = [record.name for record in query]

    return subjects


def add_new_problem(title: str, body: str, user_t_id: int, type_, is_anonymous: bool = False,
                    invite_link: str = None, group_id: int = None) -> Problem:
    user = UserModel.get_or_none(t_id=user_t_id)

    try:
        new_problem = Problem.create(title=title,
                                     body=body,
                                     user=user,
                                     is_anonymous=is_anonymous,
                                     created_at=dt.now(),
                                     type=type_,
                                     invite_link=invite_link,
                                     group_id=group_id)
    except InternalError:
        new_problem = Problem.create(title=title,
                                     body=body,
                                     user=user,
                                     is_anonymous=is_anonymous,
                                     created_at=dt.now(),
                                     type=type_,
                                     invite_link=invite_link,
                                     group_id=group_id)

    return new_problem


def get_problem_by_id(q_id) -> typing.Optional[Problem]:
    try:
        return Problem.get_or_none(id=q_id)
    except:
        return Problem.get_or_none(id=q_id)


def assign_topic(problem: Problem, subject_name: str):
    subject = Subject.get_or_none(name=subject_name)
    problem_topics = get_all_topics_for_problem(problem_id=problem.id)

    if subject.science.name not in problem_topics.keys():
        try:
            Topic.create(problem=problem, subject=subject)
        except InternalError:
            Topic.create(problem=problem, subject=subject)

        return

    if subject_name not in problem_topics.get(subject):
        try:
            Topic.create(problem=problem, subject=subject)
        except InternalError:
            Topic.create(problem=problem, subject=subject)


def get_all_open_questions() -> list:
    try:
        return list(Problem.select().where(Problem.is_closed == False))
    except InternalError:
        return list(Problem.select().where(Problem.is_closed == False))


def get_user_problems(user_t_id: int) -> list:
    try:
        user_obj = UserModel.get_or_none(t_id=user_t_id)
        return list(Problem.select().where(Problem.user == user_obj))
    except InternalError:
        user_obj = UserModel.get_or_none(t_id=user_t_id)
        return list(Problem.select().where(Problem.user == user_obj))


def get_all_topics_for_problem(problem_id: int) -> dict:
    predicate = (Problem.id == problem_id)

    query_topics = (Topic
                    .select(Topic, Problem, Subject)
                    .join(Problem, on=(Topic.problem == Problem.id))
                    .switch(Topic)
                    .join(Subject, on=(Topic.subject == Subject.id))
                    .where(predicate)
                    )

    topics = {}
    for record in query_topics:
        if topics.__contains__(record.subject.science.name):
            topics[record.subject.science.name].append(record.subject.name)
        else:
            topics[record.subject.science.name] = [record.subject.name]

    return topics


# We need to put these check-validity functions into one
def is_valid(Clazz: Science.__class__, name: str) -> bool:
    """
        Validates Science by name. If science with given name presents in db True is being returned.

    """
    if Clazz.get_or_none(name=name) is None:
        return False
    return True


def department_is_valid(name: str) -> bool:
    for department in DEPARTMENT_OPTIONS:
        if name == department[1]:
            return True
    return False


def degree_is_valid(name: str) -> bool:
    for degree in DEGREE_LEVEL_OPTIONS:
        if name == degree[1]:
            return True
    return False


def get_list_of_users_who_liked(problem_id: int) -> list:
    predicate = (Problem.id == problem_id)
    query = (ProblemLike
             .select(ProblemLike, UserModel, Problem)
             .join(Problem, on=(ProblemLike.problem == Problem.id))
             .switch(UserModel)
             .join(UserModel, on=(ProblemLike.liked_by == UserModel.id))
             .where(predicate)
             )
    liked_by_users = [record.liked_by.t_id for record in query]

    return liked_by_users


def is_problem_liked_by_user(problem_id: int, user_t_id: int) -> bool:
    try:
        liked_by_users = get_list_of_users_who_liked(problem_id)
    except InternalError:
        liked_by_users = get_list_of_users_who_liked(problem_id)

    if user_t_id in liked_by_users:
        return True
    return False


async def add_new_response(problem_id: int, body: str, user_t_id: int, is_anonymous: bool):
    try:
        user = UserModel.get_or_none(t_id=user_t_id)
        problem_obj = Problem.get_or_none(id=problem_id)
    except InternalError:
        user = UserModel.get_or_none(t_id=user_t_id)
        problem_obj = Problem.get_or_none(id=problem_id)

    try:
        resp = Response.create(problem=problem_obj,
                               body=body,
                               author=user,
                               created_at=dt.now(),
                               is_anonymous=is_anonymous,
                               )
    except:
        resp = Response.create(problem=problem_obj,
                               body=body,
                               author=user,
                               created_at=dt.now(),
                               is_anonymous=is_anonymous,
                               )

    chat_id = problem_obj.user.t_id
    mes = QUESTION_DETAIL_UPDATE_NOTIFICATION_FOR_AUTHOR.format(title=problem_obj.title,
                                                                problem_id=problem_id,
                                                                response_id=resp.id)
    await bot_instance.send_message(chat_id=chat_id, text=mes, parse_mode=types.ParseMode.MARKDOWN)
    tracker_list = get_list_of_users_who_liked(problem_id)
    broadcast_message = QUESTION_DETAIL_UPDATE_NOTIFICATION.format(title=problem_obj.title,
                                                                   problem_id=problem_id,
                                                                   response_id=resp.id)

    await make_broadcast(broadcast_message, tracker_list)


def like_problem(problem_id: int, user_t_id: int):
    problem = Problem.get_or_none(id=problem_id)

    if problem is not None:
        try:
            user = UserModel.get_or_none(t_id=user_t_id)
            ProblemLike.create(problem=problem, liked_by=user)
        except InternalError:
            user = UserModel.get_or_none(t_id=user_t_id)
            ProblemLike.create(problem=problem, liked_by=user)
    else:
        raise DoesNotExist("Problem with given id doesn't exist.")


def dislike_problem(problem_id: int, user_t_id: int):
    try:
        problem = Problem.get_or_none(id=problem_id)
    except InternalError:
        problem = Problem.get_or_none(id=problem_id)

    if problem is not None:
        try:
            user = UserModel.get_or_none(t_id=user_t_id)
            like = ProblemLike.get_or_none(problem=problem, liked_by=user)
            ProblemLike.delete_by_id(like.id)
        except InternalError:
            user = UserModel.get_or_none(t_id=user_t_id)
            like = ProblemLike.get_or_none(problem=problem, liked_by=user)
            ProblemLike.delete_by_id(like.id)
    else:
        raise DoesNotExist("Problem with given id doesn't exist.")


def get_list_of_users_who_reported_problem(problem_id: int):
    """
        Returns a list of t_ids of users who reported this problem.
    """
    predicate = (Problem.id == problem_id)
    query = (ProblemReport
             .select(ProblemReport, Problem, UserModel)
             .join(Problem, on=(ProblemReport.report_problem == Problem.id))
             .switch(UserModel)
             .join(UserModel, on=(ProblemReport.author == UserModel.id))
             .where(predicate)
             )
    print([record.author.t_id for record in query])
    return [record.author.t_id for record in query]


def is_problem_reported_by_user(problem_id: int, user_id: int):
    return user_id in get_list_of_users_who_reported_problem(problem_id)


def report_problem(problem_id: int, report_reason, report_author_id: int):
    problem = Problem.get_or_none(id=problem_id)
    report_reason_cleared = ""
    if report_reason in REPORT_REASONS_ALIASES.values():
        report_reason_cleared = report_reason
    elif report_reason in REPORT_REASONS_ALIASES.keys():
        report_reason_cleared = REPORT_REASONS_ALIASES[report_reason]
    else:
        raise KeyError("Incorrect report_reason.")

    if problem is not None:
        author_obj = UserModel.get_or_none(t_id=report_author_id)

        try:
            ProblemReport.create(report_problem=problem,
                                 author=author_obj,
                                 report_reason=report_reason_cleared,
                                 )
        except InternalError:
            ProblemReport.create(report_problem=problem,
                                 author=author_obj,
                                 report_reason=report_reason_cleared,
                                 )


def get_all_responses_for_problem(problem_id: int):
    # responses = Response.select().join(Problem).where(Problem.id == problem_id)

    return Response.select().join(Problem).where(Problem.id == problem_id)


def get_response_by_id(response_id: int) -> typing.Optional[Response]:
    return Response.get_or_none(id=response_id)


async def close_problem_via_response(response_id: int):
    response_obj = Response.get_or_none(id=response_id)
    if response_obj is not None:
        problem_obj = response_obj.problem
        problem_obj.is_closed = True
        problem_obj.save()
        response_obj.is_final = True
        response_obj.save()
        # sending notification
        r_author = response_obj.author
        mes = QUESTION_DETAIL_CLOSED_NOTIFICATION_MESSAGE.format(problem_id=problem_obj.id,
                                                                 title=problem_obj.title,
                                                                 response_id=response_id)

        await bot_instance.send_message(chat_id=r_author.t_id, text=mes, parse_mode=types.ParseMode.MARKDOWN)


async def delete_problem_by_admin(problem_id: int, reason: str):
    problem = Problem.get_or_none(id=problem_id)
    responses = get_all_responses_for_problem(problem_id)

    for response in responses:
        # delete all responses
        await delete_response_by_admin(response.id)

    topics = get_all_topics_for_problem(problem_id)
    # delete all topics related to it
    delete_topics(topics, problem_id)
    # delete all problem likes
    likes = (ProblemLike
             .select(ProblemLike, Problem, UserModel)
             .join(Problem, on=(ProblemLike.problem == Problem.id))
             .switch(UserModel)
             .join(UserModel, on=(ProblemLike.liked_by == UserModel.id))
             .where(Problem.id == problem_id))
    users_who_liked_problem = []
    for like in likes:
        try:
            ProblemLike.delete_by_id(like.id)
            users_who_liked_problem.append(like.liked_by.t_id)

        except:
            pass

    # delete all reports
    reports = (ProblemReport
               .select(ProblemReport, Problem)
               .join(Problem, on=(ProblemReport.report_problem == Problem.id))
               .where(Problem.id == problem_id))

    for report in reports:
        try:
            ProblemReport.delete_by_id(report.id)
        except:
            pass

    # sending notifications
    sub_mes = ""
    reason_mes = ""
    q_detail_temp = QUESTION_DETAIL_MESSAGE.format(id=problem.id,
                                                   title=problem.title,
                                                   author_name=("Anonymous"
                                                                if problem.is_anonymous else problem.user.name),
                                                   body=problem.body,
                                                   topics="Темы удалены.")
    dis_detail_temp = DISCUSSION_DETAIL_MESSAGE.format(id=problem.id,
                                                       title=problem.title,
                                                       author_name=("Anonymous"
                                                                    if problem.is_anonymous else problem.user.name),
                                                       body=problem.body,
                                                       topics="Темы удалены.")

    if problem.type == "question":
        sub_mes = "Вопрос, который ты отслеживаешь удалили :(\n\n" + q_detail_temp
        reason_mes = f"Ваш вопрос был удалён!\n\nПричина: {reason}\n\n" + q_detail_temp
    elif problem.type == "discussion":
        sub_mes = "Обсуждение, которое ты отслеживаешь удалили :(\n\n" + dis_detail_temp
        reason_mes = f"Ваше обсуждение было удалено!\n\nПричина: {reason}\n\n" + dis_detail_temp

        await bot_instance.send_message(chat_id=problem.group_id, text=reason_mes)
        await bot_instance.leave_chat(chat_id=problem.group_id)

    await make_broadcast(sub_mes, users_who_liked_problem)
    await bot_instance.send_message(chat_id=problem.user.t_id, text=reason_mes)

    try:
        # delete problem
        Problem.delete_by_id(problem_id)
    except:
        pass


async def delete_response_by_admin(response_id: int, send_notifications: bool = False, reason: str = None):
    if send_notifications:
        response = Response.get_or_none(id=response_id)
        response_temp = QUESTION_DETAIL_RESPONSE_MESSAGE.format(r_id=response_id,
                                                                r_author=response.author.name,
                                                                date=response.created_at,
                                                                body=response.body)
        mes = "Ваш ответ был удалён!\n\n" + response_temp + f"\n\nПричина удаления: {reason}"
        chat_id = response.author.t_id
        await bot_instance.send_message(chat_id=chat_id, text=mes)
    try:
        Response.delete_by_id(response_id)
    except:
        pass


def delete_topics(topics: dict, problem_id: int):
    print(topics)
    for science_name in topics:
        topic_list = topics[science_name]
        for topic in topic_list:
            topic_obj = Topic.get_or_none(problem_id=problem_id, subject__name=topic)
            try:
                Topic.delete_by_id(topic_obj.id)
            except:
                pass


"""
def test(problem_id: int = 1):
    reports = (ProblemReport
               .select(ProblemReport, Problem)
               .join(Problem, on=(ProblemReport.report_problem == Problem.id))
               .where(Problem.id == problem_id))
    print([rep.report_reason for rep in reports])
"""