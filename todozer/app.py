import argparse
import configparser
import datetime
import logging
import os.path
import sys

from vkostyanetsky import cliutils
from todozer import constants
from todozer import datafile, scheduler
from todozer.menu import TodozerMenu
from todozer.parser import Parser, List, Task


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
        file = open(filename, "w")
        config.write(file)

    return config


def get_uncompleted_dates(file_items: list) -> list:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    dates_in_progress = []

    for file_item in file_items:

        if type(file_item) == List and file_item.date <= yesterday:

            scheduled_tasks = file_item.get_scheduled_tasks()

            if len(scheduled_tasks) > 0:
                incomplete_day = List(file_item.lines[0])
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


def get_tasks(config: configparser.ConfigParser):

    tasks_file_name = config.get("TASKS", "tasks_file_name")

    return Parser(tasks_file_name).parse()


def get_plans(config: configparser.ConfigParser):

    plans_file_name = config.get("TASKS", "plans_file_name")

    return Parser(plans_file_name).parse()


def create_planned_tasks(menu_item_parameters: dict) -> None:
    """
    Creates tasks for the today (and days before, in case it was not done yet).

    All tasks in progress must be marked as completed, cancelled or rearranged
    to other upcoming date before the user runs the procedure.
    """

    config = menu_item_parameters.get("config")
    data = menu_item_parameters.get("data")

    tasks = get_tasks(config)

    if check_for_uncompleted_dates(tasks):

        plans = get_plans(config)
        last_date = data.get("last_date")
        tasks_lists = filter(lambda file_item: type(file_item) == List, tasks)

        for tasks_list in list(tasks_lists):

            is_date_to_plan = last_date is None or (
                tasks_list.date is not None and tasks_list.date > last_date
            )

            if is_date_to_plan:
                plan_date(tasks_list.date, plans)

    # cliutils.ask_for_enter()
    #
    # main_menu(config, data)


def plan_date(date: datetime.date, plans: list):

    for plan in plans:
        if isinstance(plan, List):
            plan_date(date, plan.items)
        elif isinstance(plan, Task):
            scheduler.match(plan.title, date)


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
            encoding=constants.encoding,
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=logging.DEBUG,
            force=True,
        )

    logging.debug("The app is started!")

    data = datafile.load()

    create_planned_tasks({"config": config, "data": data})

    # main_menu(config, data)
