import datetime

from consolemenu import *
from consolemenu.items import *

from tasks_file import *

import os.path as path


def get_tasks_file_path() -> str:
    directory = path.dirname(__file__)
    file_name = "tasks.md"

    return path.join(directory, file_name)


def get_plans_file_path() -> str:
    directory = path.dirname(__file__)
    file_name = "plans.md"

    return path.join(directory, file_name)


def tasks_in_progress(file_items: list) -> list:
    return []


def get_incomplete_days(file_items: list) -> list:
    current_date = datetime.date.today()
    incomplete_days = []

    for file_item in file_items:

        if type(file_item) == Date and file_item.date <= current_date:

            scheduled_tasks = file_item.get_scheduled_tasks()

            if len(scheduled_tasks) > 0:
                incomplete_day = Date(file_item.lines[0])
                incomplete_day.items = scheduled_tasks

                incomplete_days.append(incomplete_day)

    return incomplete_days


def update_tasks() -> None:
    """
    Creates tasks for the current day (and days before, in case the script wasn't called for them previously),
    according to the tasks file (tasks.md by default) & the plans file (plans.md by default).

    All tasks in progress must be marked as completed, cancelled or rearranged to other upcoming date
    before the user runs the procedure.
    """

    tasks_file_path = get_tasks_file_path()

    file_items = Parser(tasks_file_path).parse()

    incomplete_days = get_incomplete_days(file_items)

    if len(incomplete_days) > 0:

        print("Unable to perform, since there is at least one incomplete task:\n")

        for incomplete_day in incomplete_days:
            print(incomplete_day)
            print()

        print("You have to rearrange it or mark it as complete or cancelled.")


def trigger_menu_item_update_tasks(prompt_utils: PromptUtils):

    update_tasks()

    prompt_utils.enter_to_continue()


def display_menu() -> None:
    """
    Builds and then displays the main menu of the application.
    """

    prompt_utils = PromptUtils(Screen())

    the_quote = "Life is like riding a bicycle.\nTo keep your balance you must keep moving.\n— Albert Einstein"
    main_menu = ConsoleMenu("ORGANIZER", the_quote)

    main_menu.append_item(
        FunctionItem("Update tasks", update_tasks, [prompt_utils])
    )

    main_menu.show()


if __name__ == '__main__':
    #display_menu()
    update_tasks()
