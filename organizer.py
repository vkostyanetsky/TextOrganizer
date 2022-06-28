import datetime
import os.path as path

from consolemenu import ConsoleMenu, PromptUtils, Screen
from consolemenu.items import FunctionItem

from tasks_file import Date, Parser
from history_file import HistoryFile


def get_tasks_file_path() -> str:
    directory = path.dirname(__file__)
    file_name = "tasks.md"

    return path.join(directory, file_name)


def get_plans_file_path() -> str:
    directory = path.dirname(__file__)
    file_name = "plans.md"

    return path.join(directory, file_name)


def get_history_file_path() -> str:
    directory = path.dirname(__file__)
    file_name = "history.yaml"

    return path.join(directory, file_name)


def get_dates_in_progress(file_items: list) -> list:
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


def check_for_dates_in_progress(file_items: list) -> bool:
    passed = True

    dates_in_progress = get_dates_in_progress(file_items)

    if len(dates_in_progress) > 0:

        print("Unable to perform, since there is at least one task in progress:\n")

        for date_in_progress in dates_in_progress:
            print(date_in_progress)
            print()

        print("You have to rearrange it or mark it as completed or cancelled.")
        print()

        passed = False

    return passed


def update_tasks() -> None:
    """
    Creates tasks for the current day (and days before, in case the script
    wasn't called for them previously), according to the tasks file
    (tasks.md by default) & the plans file (plans.md by default).

    All tasks in progress must be marked as completed, cancelled
    or rearranged to other upcoming date before the user
    runs the procedure.
    """

    tasks_file_path = get_tasks_file_path()
    history_file_path = get_history_file_path()

    file_items = Parser(tasks_file_path).parse()

    if check_for_dates_in_progress(file_items):
        history = HistoryFile(history_file_path)

        for day in list(filter(lambda file_item: type(file_item) == Date, file_items)):
            if day.date not in history.planned_dates:
                print(day.date)

    # TODO Need to find dates without a "done" mark and fill them.


def trigger_menu_item_update_tasks(prompt_utils: PromptUtils):
    update_tasks()

    prompt_utils.enter_to_continue()


def display_menu() -> None:
    """
    Builds and then displays the main menu of the application.
    """

    prompt_utils = PromptUtils(Screen())

    the_quote = """
    Life is like riding a bicycle.
    To keep your balance you must keep moving.
    — Albert Einstein
    """
    main_menu = ConsoleMenu("ORGANIZER", the_quote)

    main_menu.append_item(
        FunctionItem("Create Tasks for Today", trigger_menu_item_update_tasks, [prompt_utils])
    )

    main_menu.show()


if __name__ == "__main__":
    display_menu()
