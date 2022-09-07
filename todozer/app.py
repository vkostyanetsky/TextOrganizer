import argparse
import datetime
import logging
import os
import sys
from logging import config

from vkostyanetsky import cliutils

from todozer import utils
from todozer.menu import TodozerMenu
from todozer.parser import Date, Parser


def get_arguments() -> argparse.Namespace:

    args_parser = argparse.ArgumentParser(description="TODOZER")

    args_parser.add_argument(
        "-o",
        "--options",
        type=str,
        default="options.yaml",
        help="configuration file name (default: options.yaml)",
    )

    args_parser.add_argument(
        "-l",
        "--logging",
        type=str,
        help="logging configuration file name",
    )

    return args_parser.parse_args()


def get_storage_file_name() -> str:
    return "todozer.yaml"


def load_storage() -> dict:
    file_name = get_storage_file_name()
    return utils.load_yaml(file_name)


def save_storage(file_data: dict) -> None:
    file_name = get_storage_file_name()
    utils.save_yaml(file_name, file_data)


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

    options = menu_item_parameters.get("options")
    storage = menu_item_parameters.get("storage")

    tasks_file_name = options.get("tasks_file_name")
    tasks_file_items = Parser(tasks_file_name).parse()

    if check_for_uncompleted_dates(tasks_file_items):

        plans_file_name = options.get("plans_file_name")
        plans_file_items = Parser(plans_file_name).parse()

        last_date = storage.get("last_date")

        days = filter(lambda file_item: type(file_item) == Date, tasks_file_items)

        for day in list(days):

            if last_date is None or day.date > last_date:
                print(day.date)

    cliutils.ask_for_enter()

    main_menu(options, storage)

    # TODO Need to find dates without a "done" mark and fill them.
    # TODO Read existing tasks, add planned, sort all of them, then write.
    # TODO Logging to text files
    # TODO Output tasks & plans healthcheck before main menu showing in case something is wrong


def statistics(menu_item_parameters: dict) -> None:

    sys.exit(0)


def main_menu(options: dict, storage: dict) -> None:
    """
    Builds and then displays the main menu of the application.
    """

    menu = TodozerMenu()

    menu_item_parameters = {"options": options, "storage": storage}

    menu.add_item("Create Planned Tasks", create_planned_tasks, menu_item_parameters)
    menu.add_item("Statistics", statistics, menu_item_parameters)
    menu.add_item("Exit", sys.exit)

    menu.choose()


def main():

    arguments = get_arguments()

    if arguments.logging is not None:
        if os.path.exists(arguments.logging):
            logging_config = utils.load_yaml(arguments.logging)
            config.dictConfig(logging_config)

    options = utils.load_yaml(arguments.options)
    storage = load_storage()

    logging.debug("Hi!")

    main_menu(options, storage)
