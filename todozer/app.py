import argparse
import configparser
import datetime
import logging
import os.path
import sys

from vkostyanetsky import cliutils

from todozer import datafile, scheduler
from todozer.menu import TodozerMenu
from todozer.parser import Date, Parser, Task


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
            "LOG": {"write_log": True, "file_name": "todozer.log", "file_mode": "w"},
        }
    )

    if os.path.exists(filename):
        config.read(filename)
    else:
        file = open(filename, "w")
        config.write(file)

    return config


def get_uncompleted_dates(file_items: list) -> list:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    dates_in_progress = []

    for file_item in file_items:

        if type(file_item) == Date and file_item.date <= yesterday:

            scheduled_tasks = file_item.get_scheduled_tasks()

            if len(scheduled_tasks) > 0:
                incomplete_day = Date(file_item.lines[0])
                incomplete_day.items = scheduled_tasks

                dates_in_progress.append(incomplete_day)

    return dates_in_progress


def check_for_uncompleted_dates(tasks_file_items: list) -> bool:

    passed = True

    dates_in_progress = get_uncompleted_dates(tasks_file_items)

    if len(dates_in_progress) > 0:

        passed = False

        print("Unable to perform, since there is at least one task in progress:")
        print()

        for date_in_progress in dates_in_progress:
            print(date_in_progress)
            print()

        print(
            "You have to rearrange tasks in progress"
            " or mark them as completed or cancelled."
        )
        print()

    return passed


def create_planned_tasks(menu_item_parameters: dict) -> None:
    """
    Creates tasks for the today (and days before, in case it was not done yet).

    All tasks in progress must be marked as completed, cancelled or rearranged
    to other upcoming date before the user runs the procedure.
    """

    config = menu_item_parameters.get("config")
    data = menu_item_parameters.get("data")

    tasks_file_name = config.get("TASKS", "tasks_file_name")
    tasks_file_items = Parser(tasks_file_name).parse()

    if check_for_uncompleted_dates(tasks_file_items):

        plans_file_name = config.get("TASKS", "plans_file_name")
        plans_file_items = Parser(plans_file_name).parse()

        last_date = data.get("last_date")

        days = filter(lambda file_item: type(file_item) == Date, tasks_file_items)

        for day in list(days):

            if last_date is None or day.date > last_date:

                plans = filter(
                    lambda file_item: type(file_item) == Task, plans_file_items
                )

                for plan in plans:
                    scheduler.match(plan.title, day.date)

    cliutils.ask_for_enter()

    main_menu(config, data)


def statistics(menu_item_parameters: dict) -> None:

    sys.exit(0)


def main_menu(config: configparser.ConfigParser, data: dict) -> None:
    """
    Builds and then displays the main menu of the application.
    """

    menu = TodozerMenu()

    menu_item_parameters = {"config": config, "data": data}

    menu.add_item("Create Planned Tasks", create_planned_tasks, menu_item_parameters)
    menu.add_item("Statistics", statistics, menu_item_parameters)
    menu.add_item("Exit", sys.exit)

    menu.choose()


def main():

    arguments = get_arguments()

    config = get_config(arguments.config)

    if config.getboolean("LOG", "write_log"):

        logging.basicConfig(
            filename=config.get("LOG", "file_name"),
            filemode=config.get("LOG", "file_mode"),
            encoding="utf-8",
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=logging.DEBUG,
            force=True,
        )

    logging.debug("The app is started!")

    data = datafile.load()

    main_menu(config, data)
