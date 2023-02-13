#!/usr/bin/env python3

import datetime

from todozer import constants, task_lists
from todozer.todo import task_todo


def get_active_task(
    session: dict, tasks_file_items: list = None
) -> task_todo.TaskTodo | None:
    """
    Returns an active task for a current day, if a timer is running somewhere.
    """

    result = None

    running_timer_date = session["state"]["running_timer_date"]

    if running_timer_date is not None:
        if tasks_file_items is None:
            tasks_file_items = task_lists.load_tasks_file_items(session["config"])

        tasks_list = task_lists.get_tasks_list_by_date(
            tasks=tasks_file_items, date=running_timer_date
        )

        if tasks_list is not None:
            result = tasks_list.get_active_task()

    return result


def get_date_from_string(source: str) -> datetime.date:
    return datetime.datetime.strptime(source, constants.DATE_FORMAT).date()


def get_string_from_date(source: datetime.date) -> str:
    return source.strftime(constants.DATE_FORMAT)


def get_month_last_day_date(date: datetime.date) -> datetime.date:
    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def get_date_of_yesterday(today: datetime.date = None) -> datetime.date:
    if today is None:
        today = get_date_of_today()

    return today - datetime.timedelta(days=1)


def get_date_of_today() -> datetime.date:
    return datetime.date.today()


def get_date_of_tomorrow(today: datetime.date = None) -> datetime.date:
    if today is None:
        today = get_date_of_today()

    return today + datetime.timedelta(days=1)


def get_regexp_for_date() -> str:
    """
    Returns regular expression for a standard date (YYYY-MM-DD).
    """
    return "[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}"


def get_previous_day_of_week(
    day_index: int, date: datetime.date = None
) -> datetime.date:
    if date is None:
        date = datetime.date.today()

    previous_day = date

    while previous_day.weekday() != day_index:
        previous_day -= datetime.timedelta(days=1)

    return previous_day


def get_next_day_of_week(day_index: int, date: datetime.date = None) -> datetime.date:
    if date is None:
        date = datetime.date.today()

    next_day = date

    while next_day.weekday() != day_index:
        next_day += datetime.timedelta(days=1)

    return next_day
