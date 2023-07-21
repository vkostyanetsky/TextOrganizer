#!/usr/bin/env python3

import os

"""Methods to work with task lists in tasks file & plans file."""

import configparser
import datetime

from todozer import constants, parser, scheduler, utils
from todozer.todo import list_todo, plan_todo, task_todo


def save_tasks_file_items(tasks_file_items: list, config: configparser.ConfigParser, path: str | None):
    content = []

    tasks_file_items = sorted(
        tasks_file_items,
        key=lambda item: item.date,
        reverse=bool(config.getboolean("TASKS", "reverse_days_order")),
    )

    for tasks_file_item in tasks_file_items:
        content.append(str(tasks_file_item))

    tasks_file_name = config.get("TASKS", "file_name")

    if path is not None:
        tasks_file_name = os.path.join(path, tasks_file_name)

    with open(tasks_file_name, "w", encoding=constants.ENCODING) as tasks_file:
        tasks_file.write("\n\n".join(content))


def load_tasks_file_items(config: configparser.ConfigParser, path: str):
    tasks_file_name = config.get("TASKS", "file_name")

    if path is not None:
        tasks_file_name = os.path.join(path, tasks_file_name)

    tasks_file_items = parser.Parser(tasks_file_name, task_todo.TaskTodo).parse()

    return sorted(tasks_file_items, key=lambda item: item.date)


def load_plans_file_items(config: configparser.ConfigParser, path: str):
    plans_file_name = config.get("PLANS", "file_name")

    if path is not None:
        plans_file_name = os.path.join(path, plans_file_name)

    return parser.Parser(plans_file_name, plan_todo.PlanTodo).parse()


def get_task_lists_in_progress(file_items: list) -> list:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    dates_in_progress = []

    for file_item in file_items:
        if type(file_item) == list_todo.ListTodo and file_item.date <= yesterday:
            scheduled_tasks = file_item.get_scheduled_tasks()

            if scheduled_tasks:
                incomplete_day = list_todo.ListTodo(file_item.lines[0])
                incomplete_day.items = scheduled_tasks

                dates_in_progress.append(incomplete_day)

    return dates_in_progress


def fill_tasks_lists(task_items: list, plan_items: list, data: dict) -> list:
    filled_list_titles = []

    today = utils.get_date_of_today()

    for task_item in task_items:
        is_list_to_fill = (
            type(task_item) == list_todo.ListTodo
            and task_item.date is not None
            and data["last_planning_date"] < task_item.date <= today
        )

        if is_list_to_fill:
            fill_tasks_list(task_item, plan_items)

            filled_list_titles.append(task_item.title)

    return filled_list_titles


def fill_tasks_list(
    tasks_file_item: list_todo.ListTodo, plans_file_items: list
) -> None:
    for plans_file_item in plans_file_items:
        if isinstance(plans_file_item, list_todo.ListTodo):
            fill_tasks_list(tasks_file_item, plans_file_item.items)

        elif isinstance(plans_file_item, plan_todo.PlanTodo):
            _, is_date_matched = scheduler.match(plans_file_item, tasks_file_item.date)

            if is_date_matched:
                line = f"- [ ] {plans_file_item.title}"
                task = task_todo.TaskTodo(line)

                if len(plans_file_item.lines) > 1:
                    i = 0

                    for plan_line in plans_file_item.lines:
                        i += 1

                        if i == 1:
                            continue

                        task.lines.append(plan_line)

                tasks_file_item.items.append(task)

    tasks_file_item.sort_tasks()


def add_tasks_lists(tasks: list, last_date: datetime.date) -> None:
    date = utils.get_date_of_tomorrow(last_date)
    today = utils.get_date_of_today()

    while date <= today:
        if not get_tasks_list_by_date(tasks, date):
            date_string = utils.get_string_from_date(date)
            line = f"# {date_string}"
            tasks.append(list_todo.ListTodo(line))

        date = utils.get_date_of_tomorrow(date)


def get_tasks_list_by_date(
    tasks: list, date: datetime.date
) -> list_todo.ListTodo | None:
    # TODO probably better to do it like .is_date (duck typing)
    lists = list(
        filter(
            lambda item: type(item) is list_todo.ListTodo and item.date == date, tasks
        )
    )

    return lists[0] if lists else None
