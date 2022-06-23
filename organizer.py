import datetime

from consolemenu import *
from consolemenu.items import *

from tasks_file_format import *
from tasks_file_parser import *

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


def update_tasks() -> None:
    """
    Creates tasks for the current day (and days before, in case the script wasn't called for them previously),
    according to the tasks file (tasks.md by default) & the plans file (plans.md by default).

    All tasks in progress must be marked as completed, cancelled or rearranged to other upcoming date
    before the user runs the procedure.
    """

    tasks_file_path = get_tasks_file_path()

    file_items = TasksFileParser(tasks_file_path).parse()

    current_date = datetime.date.today()

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
