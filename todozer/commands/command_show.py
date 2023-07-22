#!/usr/bin/env python3

"""Simply outputs tasks for a given date and quits."""

import datetime

import click
from vkostyanetsky import cliutils

from todozer import state_file, task_lists, utils
from todozer.todo import list_todo


def main(what: str, detail: str, path: str | None) -> None:
    """
    Checks plans file for errors.
    """

    config = utils.get_config(path)
    utils.set_logging(config)

    state = state_file.load(path)

    tasks = task_lists.load_tasks_file_items(config, path)
    plans = task_lists.load_plans_file_items(config, path)

    if what == "today":
        __show_today(tasks, plans, state)
    elif what == "last":
        __show_last_n_days(tasks, plans, state, days_number=int(detail))
    elif what == "next":
        __show_next_n_days(tasks, plans, state, days_number=int(detail))
    elif what == "date":
        __show_date(tasks, plans, state, date=detail)


def __show_today(tasks, plans, state) -> None:
    date = utils.get_date_of_today()
    print_tasks_by_date(date, tasks, plans, state, False)
    click.echo()


def __show_last_n_days(tasks, plans, state, days_number: int) -> None:
    date = utils.get_date_of_today() - datetime.timedelta(days=days_number)
    for _ in range(days_number):
        print_tasks_by_date(date, tasks, plans, state, False)
        date += datetime.timedelta(days=1)
        click.echo()


def __show_next_n_days(tasks, plans, state, days_number: int) -> None:
    date = utils.get_date_of_today()
    for _ in range(days_number):
        date += datetime.timedelta(days=1)
        print_tasks_by_date(date, tasks, plans, state, False)
        click.echo()


def __show_date(tasks, plans, state, date: str) -> None:
    date = utils.get_date_from_string(date)
    print_tasks_by_date(date, tasks, plans, state, False)
    click.echo()


def print_tasks_by_date(date, tasks, plans, state, time_mode) -> None:
    title = utils.get_string_from_date(date)

    click.echo(f"# {title}")
    click.echo()

    tasks_list = task_lists.get_tasks_list_by_date(tasks, date)

    if tasks_list is None:
        tasks.append(list_todo.ListTodo(f"# {title}"))
        tasks_list = tasks[-1]

    if date > state["last_planning_date"]:
        task_lists.fill_tasks_list(tasks_list, plans)

    if tasks_list.items:
        for task in tasks_list.items:
            timer_string = task.timer_string
            if time_mode:
                if timer_string == "":
                    continue

            if timer_string != "":
                timer_string = f" ({timer_string})"

            click.echo(f"{task.title_line}{timer_string}")

    else:
        click.echo("No tasks found.")


if __name__ == "__main__":
    main(what="today", detail="", path=None)
