#!/usr/bin/env python3

"""Simply outputs tasks for a given date and quits."""

import click
from vkostyanetsky import cliutils

from todozer import task_lists, utils


def main(days: str, path: str = None) -> None:
    """
    Checks plans file for errors.
    """

    config = utils.get_config(path)
    utils.set_logging(config)

    config = utils.get_config(path)
    utils.set_logging(config)

    tasks_file_items = task_lists.load_tasks_file_items(config, path)
    plans_file_items = task_lists.load_plans_file_items(config, path)

    planned_dates = []

    date = utils.get_date_of_today()

    print_tasks_by_date(date, tasks_file_items, plans_file_items, planned_dates, False)

    click.echo()

    cliutils.ask_for_enter()


def print_tasks_by_date(date, tasks, plans, planned_dates, time_mode) -> None:

    title = utils.get_string_from_date(date)

    click.echo(f"# {title}")
    click.echo()

    tasks_list = task_lists.get_tasks_list_by_date(tasks, date)

    if tasks_list is None:
        tasks.append(list_todo.ListTodo(f"# {title}"))
        tasks_list = tasks[-1]

    if date > utils.get_date_of_today():
        if date not in planned_dates:
            fill_tasks_list(tasks_list, plans)
            planned_dates.append(date)

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
    main()
