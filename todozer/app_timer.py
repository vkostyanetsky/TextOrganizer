#!/usr/bin/env python3

from vkostyanetsky import cliutils

from todozer import app, state_file, task_lists, utils
from todozer.todo import task_todo
from todozer import constants


def main_menu(session: dict) -> None:
    """
    Displays a submenu to track time.
    """

    active_task = get_active_task(session)

    texts = [constants.TITLE]

    if active_task is not None:
        texts.append(active_task.title)

    menu = cliutils.Menu(texts)

    menu.add_item("Start Timer", start_timer, session)
    menu.add_item("Stop Timer", stop_timer, session)

    menu.add_item("Back", app.main_menu, session)

    menu.choose()


def start_timer(session: dict) -> None:

    tasks_file_items = task_lists.load_tasks_file_items(session["config"])
    tasks_in_progress = get_tasks_in_progress_for_today(tasks_file_items)

    if tasks_in_progress:

        task = get_chosen_task(tasks_in_progress)

        if task is not None:

            task.start_timer()

            task_lists.save_tasks_file_items(tasks_file_items, session["config"])

            session["state"]["running_timer_date"] = utils.get_date_of_today()
            state_file.save(session["state"])

    else:
        print("No tasks in progress to track time today.")
        print()

        cliutils.ask_for_enter()

    main_menu(session)


def get_tasks_in_progress_for_today(tasks_file_items) -> list:
    result = []

    tasks_list = task_lists.get_tasks_list_by_date(
        tasks=tasks_file_items, date=utils.get_date_of_today()
    )

    if tasks_list is not None:
        for task in tasks_list.items:
            if task.is_scheduled:
                result.append(task)

    return result


def get_active_task(session: dict, tasks_file_items: list = None) -> task_todo.TaskTodo | None:
    """
    Returns an active task for a current day, if a timer is running somewhere.
    """

    result = None

    running_timer_date = session["state"]["running_timer_date"]

    if running_timer_date is not None:

        if tasks_file_items is None:
            tasks_file_items = task_lists.load_tasks_file_items(session["config"])

        tasks_list = task_lists.get_tasks_list_by_date(tasks=tasks_file_items, date=running_timer_date)

        if tasks_list is not None:
            result = tasks_list.get_active_task()

    return result


def stop_timer(session: dict) -> None:

    tasks_file_items = task_lists.load_tasks_file_items(session["config"])
    active_task = get_active_task(session, tasks_file_items)

    if active_task is not None:

        active_task.stop_timer()

        task_lists.save_tasks_file_items(tasks_file_items, session["config"])

        session["state"]["running_timer_date"] = None
        state_file.save(session["state"])

        print("The active timer has been stopped.")

    else:

        print("There is no active timer to stop.")

    print()

    cliutils.ask_for_enter()

    main_menu(session)


def get_chosen_task(tasks: list) -> task_todo.TaskTodo:

    result = None

    while result is None:

        cliutils.clear_terminal()

        for task_index in range(len(tasks)):
            print(f"{task_index + 1} - {tasks[task_index].title}")

        print()

        message = "Enter a task number to track time for: "
        user_input = cliutils.ask_for_enter(message).strip()

        if user_input == "":
            break

        if not user_input.isdigit():
            continue

        task_number = int(user_input)

        result = tasks[task_number - 1] if 0 < task_number < len(tasks) else None

    return result
