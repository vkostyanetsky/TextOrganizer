from format import *

from consolemenu import *
from consolemenu.items import *


def get_items_from_file(tasks_file_path: str) -> list:

    tasks_file = open(tasks_file_path, "r", encoding="utf-8-sig")
    file_items = []

    with tasks_file:
        while True:
            line = tasks_file.readline()

            if not line:
                break

            line = line.strip()

            if Date.match(line):

                file_item = Date(line)
                file_items.append(file_item)

            elif Task.match(line):

                file_item = Task(line)
                file_items.append(file_item)

            else:

                last_item = file_items[-1] if len(file_items) > 0 else None

                if type(last_item) == Task:
                    file_items[-1].lines.append(line)
                else:
                    file_item = Text(line)
                    file_items.append(file_item)

    return file_items


def update_tasks(prompt_utils):
    """
    Creates tasks for the current day (and days before, in case the script wasn't called for them previously),
    according to the tasks file (tasks.md by default) & the plans file (plans.md by default).

    All tasks in progress must be marked as completed, cancelled or rearranged to other upcoming date
    before the user runs the procedure.
    """

    tasks_file_path = get_tasks_file_path()

    for item in get_items_from_file(tasks_file_path):
        print(item)

    prompt_utils.enter_to_continue()


def display_menu():
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
    display_menu()
