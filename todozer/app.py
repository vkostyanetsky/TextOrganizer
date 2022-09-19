#!/usr/bin/env python3

import argparse
import configparser
import logging
import os.path
import sys
from collections import namedtuple

from vkostyanetsky import cliutils

from todozer import (constants, datafile, menu, parser, scheduler, task_lists,
                     utils)


def get_arguments() -> argparse.Namespace:

    args_parser = argparse.ArgumentParser(description="TODOZER KNOWS THE DRILL!")

    args_parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="todozer.cfg",
        help="configuration file name (default: todozer.cfg)",
    )

    return args_parser.parse_args()


def get_config(filename: str) -> configparser.ConfigParser:

    config = configparser.ConfigParser()

    config.read_dict(
        {
            "TASKS": {
                "tasks_file_name": "tasks.md",
                "plans_file_name": "plans.md",
            },
            "LOG": {"write_log": False, "file_name": "todozer.log", "file_mode": "w"},
        }
    )

    if os.path.exists(filename):
        config.read(filename)
    else:
        with open(filename, "w") as file:
            config.write(file)

    return config


def load_tasks_file_items(config: configparser.ConfigParser):

    tasks_file_name = config.get("TASKS", "tasks_file_name")

    tasks_file_items = parser.Parser(tasks_file_name, parser.Task).parse()

    return sorted(tasks_file_items, key=lambda item: item.date)


def save_tasks_file_items(tasks_file_items: list, config: configparser.ConfigParser):

    content = []

    for tasks_file_item in tasks_file_items:
        content.append(str(tasks_file_item))

    tasks_file_name = config.get("TASKS", "tasks_file_name")

    with open(tasks_file_name, "w", encoding=constants.ENCODING) as tasks_file:
        tasks_file.write("\n\n".join(content))


def load_plans_file_items(config: configparser.ConfigParser):

    plans_file_name = config.get("TASKS", "plans_file_name")

    return parser.Parser(plans_file_name, parser.Plan).parse()


def check_plans_file_items(plans_file_items: list, plans_file_issues: list):

    today = utils.get_date_of_today()

    for item in plans_file_items:

        if type(item) == parser.List:

            check_plans_file_items(item.items, plans_file_issues)

        elif type(item) == parser.Plan:

            matched_pattern, _ = scheduler.match(item, today)

            if matched_pattern == scheduler.Pattern.NONE:

                issue_text = (
                    f'Unable to match pattern for a "{item.title}" plan'
                    f' (pattern text: "{item.pattern}")'
                )

                plans_file_issues.append(issue_text)


def check_for_tasks_in_progress(tasks_file_items: list) -> bool:

    passed = True

    dates_in_progress = task_lists.get_task_lists_in_progress(tasks_file_items)

    if dates_in_progress:

        passed = False

        print("Unable to perform, since there is at least one task in progress (-):")
        print()

        for date_in_progress in dates_in_progress:
            print(date_in_progress)
            print()

        print("You have to rearrange tasks in progress or mark them as completed (+).")
        print()

    return passed


def create_planned_tasks(app: namedtuple) -> None:
    """
    Creates tasks for the today (and days before, in case it was not done yet).

    All tasks in progress must be marked as completed or rearranged
    to other upcoming date before the user runs the procedure.
    """

    logging.debug("Creating planned tasks...")

    tasks_file_items = load_tasks_file_items(app.config)
    plans_file_items = load_plans_file_items(app.config)

    task_lists.add_tasks_lists(tasks_file_items, app.data["last_date"])

    if check_for_tasks_in_progress(tasks_file_items):

        filled_list_titles = task_lists.fill_tasks_lists(
            tasks_file_items, plans_file_items, app.data
        )

        if filled_list_titles:

            save_tasks_file_items(tasks_file_items, app.config)

            app.data["last_date"] = utils.get_date_of_today()
            datafile.save(app.data)

            scheduled_tasks = ", ".join(filled_list_titles)

            print(f"Tasks for {scheduled_tasks} have been successfully scheduled.")

        else:

            print("Unable to perform, since there are no days to plan tasks.")

        print()

    cliutils.ask_for_enter()

    main_menu(app)


def tasks_browser(app: namedtuple) -> None:
    sys.exit(1)


def health_check(app: namedtuple) -> None:
    logging.debug("Checking planned tasks...")

    plans_file_items = load_plans_file_items(app.config)
    plans_file_issues = []

    check_plans_file_items(plans_file_items, plans_file_issues)

    if plans_file_issues:
        print("Issues found in the plans file:")
        print()

        for issue in plans_file_issues:
            print(f"- {issue}")

    else:
        print("Everything seems nice and clear!")

    print()

    cliutils.ask_for_enter()

    main_menu(app)


def main_menu(app: namedtuple) -> None:
    """
    Builds and then displays the main menu of the application.
    """

    todozer_menu = menu.TodozerMenu()

    todozer_menu.add_item("Create Planned Tasks", create_planned_tasks, app)
    todozer_menu.add_item("Tasks Browser", tasks_browser, app)
    todozer_menu.add_item("Health Check", health_check, app)
    todozer_menu.add_item("Exit", sys.exit)

    todozer_menu.choose()


def main():

    arguments = get_arguments()

    config = get_config(arguments.config)

    if config.getboolean("LOG", "write_log"):

        logging.basicConfig(
            filename=config.get("LOG", "file_name"),
            filemode=config.get("LOG", "file_mode"),
            encoding=constants.ENCODING,
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=logging.DEBUG,
            force=True,
        )

    data = datafile.load()

    TodozerApp = namedtuple("TodozerApp", "config data")
    app = TodozerApp(config=config, data=data)

    logging.debug("Initialization completed.")

    main_menu(app)
