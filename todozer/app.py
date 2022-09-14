import argparse
import configparser
import datetime
import logging
import os.path
import sys

from vkostyanetsky import cliutils

from todozer import constants, datafile, scheduler, utils, parser, menu


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


def set_up_logging(config: configparser.ConfigParser) -> None:

    if config.getboolean("LOG", "write_log"):

        logging.basicConfig(
            filename=config.get("LOG", "file_name"),
            filemode=config.get("LOG", "file_mode"),
            encoding=constants.ENCODING,
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=logging.DEBUG,
            force=True,
        )


def get_uncompleted_dates(file_items: list) -> list:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    dates_in_progress = []

    for file_item in file_items:

        if type(file_item) == parser.List and file_item.date <= yesterday:

            scheduled_tasks = file_item.get_scheduled_tasks()

            if len(scheduled_tasks) > 0:
                incomplete_day = parser.List(file_item.lines[0])
                incomplete_day.items = scheduled_tasks

                dates_in_progress.append(incomplete_day)

    return dates_in_progress


def check_for_uncompleted_dates(tasks_file_items: list) -> bool:

    passed = True

    dates_in_progress = get_uncompleted_dates(tasks_file_items)

    if len(dates_in_progress) > 0:

        passed = False

        print("Unable to perform, since there is at least one task in progress (*):")
        print()

        for date_in_progress in dates_in_progress:
            print(date_in_progress)
            print()

        print(
            "You have to rearrange tasks in progress"
            " or mark them as completed (+) or cancelled (-)."
        )
        print()

    return passed


def load_tasks_file_items(config: configparser.ConfigParser):

    tasks_file_name = config.get("TASKS", "tasks_file_name")

    return parser.Parser(tasks_file_name, parser.Task).parse()


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


def create_planned_tasks(menu_item_parameters: dict) -> None:
    """
    Creates tasks for the today (and days before, in case it was not done yet).

    All tasks in progress must be marked as completed, cancelled or rearranged
    to other upcoming date before the user runs the procedure.
    """

    logging.debug("Creating planned tasks...")

    config = menu_item_parameters.get("config")
    data = menu_item_parameters.get("data")

    tasks_file_items = load_tasks_file_items(config)

    add_tasks_lists(tasks_file_items, data["last_date"])

    plans_file_items = load_plans_file_items(config)

    if check_for_uncompleted_dates(tasks_file_items):

        filled_list_titles = fill_tasks_lists(tasks_file_items, plans_file_items, data)

        if filled_list_titles:

            save_tasks_file_items(tasks_file_items, config)

            data["last_date"] = utils.get_date_of_today()
            datafile.save(data)

            print(
                f"Tasks for {', '.join(filled_list_titles)} have been successfully scheduled."
            )

        else:

            print("Unable to perform, since there are no days to plan tasks.")

        print()

    cliutils.ask_for_enter()

    main_menu(config, data)


def add_tasks_lists(tasks: list, last_date: datetime.date):

    date = utils.get_date_of_tomorrow(last_date)
    today = utils.get_date_of_today()

    while date <= today:

        if (
            len(
                list(
                    filter(
                        lambda item: type(item) == parser.List and item.date == date,
                        tasks,
                    )
                )
            )
            == 0
        ):

            date_string = utils.get_string_from_date(date)
            line = f"# {date_string}"
            tasks.append(parser.List(line))

        date = utils.get_date_of_tomorrow(date)


def fill_tasks_lists(tasks_file_items: list, plans_file_items: list, data: dict) -> list:

    filled_list_titles = []

    for tasks_file_item in tasks_file_items:

        if (
            type(tasks_file_item) == parser.List
            and tasks_file_item.date is not None
            and tasks_file_item.date > data["last_date"]
        ):
            fill_tasks_list(tasks_file_item, plans_file_items)
            sort_tasks_list(tasks_file_item)

            filled_list_titles.append(tasks_file_item.title)

    return filled_list_titles


def sort_tasks_list(tasks_file_item: parser.List):

    tasks_file_item.items = sorted(tasks_file_item.items, key=lambda item: item.time)


def fill_tasks_list(tasks_file_item: parser.List, plans_file_items: list):

    for plans_file_item in plans_file_items:

        if isinstance(plans_file_item, parser.List):
            fill_tasks_list(tasks_file_item, plans_file_item.items)
        elif isinstance(plans_file_item, parser.Plan):
            if scheduler.match(plans_file_item, tasks_file_item.date) is not None:
                line = f"{parser.Task.scheduled_task_mark}{plans_file_item.title}"
                task = parser.Task(line)
                if len(plans_file_item.lines) > 1:
                    i = 0
                    for plan_line in plans_file_item.lines:
                        i += 1
                        if i == 1:
                            continue
                        task.lines.append(plan_line)
                tasks_file_item.items.append(task)


def statistics(menu_item_parameters: dict) -> None:

    sys.exit(0)


def main_menu(config: configparser.ConfigParser, data: dict) -> None:
    """
    Builds and then displays the main menu of the application.
    """

    todozer_menu = menu.TodozerMenu()

    menu_item_parameters = {"config": config, "data": data}

    todozer_menu.add_item(
        "Create Planned Tasks", create_planned_tasks, menu_item_parameters
    )
    todozer_menu.add_item("Statistics", statistics, menu_item_parameters)
    todozer_menu.add_item("Exit", sys.exit)

    todozer_menu.choose()


def main():

    arguments = get_arguments()

    config = get_config(arguments.config)

    set_up_logging(config)

    data = datafile.load()

    logging.debug("Initialization completed.")

    main_menu(config, data)
