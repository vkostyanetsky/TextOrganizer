#!/usr/bin/env python3

import argparse
import configparser
import datetime
import logging
import os.path
import sys
from collections import namedtuple

from vkostyanetsky import cliutils

from todozer import (
    constants,
    datafile,
    menu,
    parser,
    scheduler,
    task_lists,
    utils,
    timer,
)


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


def main_menu(app: namedtuple) -> None:
    """
    Displays the main menu of the application.
    """

    todozer_menu = menu.TodozerMenu()

    todozer_menu.add_item("View Tasks", view_tasks, app)
    todozer_menu.add_item("Plan Tasks", plan_tasks_submenu, app)
    todozer_menu.add_item("Track Time", track_time_submenu, app)
    todozer_menu.add_item("Exit", sys.exit)

    todozer_menu.choose()


def view_tasks(app: namedtuple) -> None:
    pass


def plan_tasks_submenu(app: namedtuple) -> None:
    """
    Displays a submenu to plan tasks.
    """

    todozer_menu = menu.TodozerMenu()

    todozer_menu.add_item("Create Planned Tasks", create_planned_tasks, app)
    todozer_menu.add_item("Health Check", health_check, app)
    todozer_menu.add_item("Back", main_menu, app)

    todozer_menu.choose()


def track_time_submenu(app: namedtuple) -> None:
    """
    Displays a submenu to track time.
    """

    timers = timer.read()
    active_timer = get_active_timer(timers)

    todozer_menu = menu.TodozerMenu()

    todozer_menu.add_item("Start Timer", start_timer, app)

    if active_timer:
        todozer_menu.add_item("Stop Timer", stop_timer, app)

    todozer_menu.add_item("Back", main_menu, app)

    todozer_menu.choose()


def get_titles_of_tasks_in_progress_for_today(app: namedtuple) -> list:
    result = []

    tasks_list = task_lists.get_tasks_list_by_date(
        tasks=load_tasks_file_items(app.config), date=utils.get_date_of_today()
    )

    if tasks_list is not None:
        for task in tasks_list.items:
            if task.is_scheduled:
                result.append(task.title)

    return result


def get_chosen_task_title(titles: list):

    result = None

    while result is None:

        cliutils.clear_terminal()

        for title_index in range(len(titles)):
            print(f"{title_index + 1} - {titles[title_index]}")

        print()

        message = "Enter a task number to track time for: "
        user_input = cliutils.ask_for_enter(message).strip()

        if user_input == "":
            break

        if not user_input.isdigit():
            continue

        task_number = int(user_input)

        result = titles[task_number - 1] if 0 < task_number < len(titles) else None

    return result


def start_timer(app: namedtuple) -> None:

    titles = get_titles_of_tasks_in_progress_for_today(app)

    if titles:

        title = get_chosen_task_title(titles)

        if title is not None:

            records = timer.read()
            records.append(
                {"started": datetime.datetime.now(), "task": title}
            )

            timer.write(records)

    else:
        print("No tasks in progress to track time today.")
        print()

        cliutils.ask_for_enter()

    track_time_submenu(app)


def stop_timer(app: namedtuple) -> None:
    timers = timer.read()
    active_timer = get_active_timer(timers)

    if active_timer:

        active_timer['stopped'] = datetime.datetime.now()
        timer.write(timers)

        print('The active timer has been stopped.')

    else:

        print('There is no active timer to stop.')

    print()

    cliutils.ask_for_enter()

    track_time_submenu(app)


def get_active_timer(timers: list) -> dict:
    return timers[-1] if len(timers) > 0 and timers[-1].get('stopped') is None else None


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

    plan_tasks_submenu(app)


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

    plan_tasks_submenu(app)
