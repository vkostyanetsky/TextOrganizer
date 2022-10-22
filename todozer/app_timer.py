#!/usr/bin/env python3

import datetime

from vkostyanetsky import cliutils

from todozer import app, menu, parser, state_file, task_lists, utils


def main_menu(session: dict) -> None:
    """
    Displays a submenu to track time.
    """

    todozer_menu = menu.TodozerMenu()

    todozer_menu.add_item("Start Timer", start_timer, session)
    todozer_menu.add_item("Stop Timer", stop_timer, session)

    todozer_menu.add_item("Back", app.main_menu, session)

    todozer_menu.choose()


def start_timer(session: dict) -> None:

    tasks_file_items = task_lists.load_tasks_file_items(session["config"])
    tasks_in_progress = get_tasks_in_progress_for_today(tasks_file_items)

    if tasks_in_progress:

        task = get_chosen_task(tasks_in_progress)

        if task is not None:
            current_time_string = get_current_time_string()
            empty_time_string = get_empty_time_string()
            time_string = datetime.datetime.now().strftime(
                f"    {current_time_string} -> {empty_time_string}  "
            )

            task.lines.append(time_string)
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


def stop_timer(session: dict) -> None:

    running_timer_date = session["state"]["running_timer_date"]

    if running_timer_date is not None:

        tasks_file_items = task_lists.load_tasks_file_items(session["config"])

        tasks_list = task_lists.get_tasks_list_by_date(
            tasks=tasks_file_items, date=running_timer_date
        )  # TODO WHAT IF NOT FOUND?

        task_found = False

        for task in tasks_list.items:
            for line_index in range(len(task.lines)):
                line = task.lines[line_index]
                if line.find("(...)") != -1:
                    current_time_string = get_current_time_string()
                    empty_time_string = get_empty_time_string()
                    task.lines[line_index] = line.replace(
                        empty_time_string, current_time_string, 1
                    )
                    task_found = True
                    break
            if task_found:
                break

        task_lists.save_tasks_file_items(tasks_file_items, session["config"])

        session["state"]["running_timer_date"] = None
        state_file.save(session["state"])

        print("The active timer has been stopped.")

    else:

        print("There is no active timer to stop.")

    print()

    cliutils.ask_for_enter()

    main_menu(session)


def get_current_time_string() -> str:
    return datetime.datetime.now().strftime("%H:%M")


def get_empty_time_string() -> str:
    return "(...)"


# def get_active_timer(timers: list) -> dict:
#     return timers[-1] if len(timers) > 0 and timers[-1].get("stopped") is None else None
#
#
# def read() -> list:
#     """
#     Reads records from the file.
#     """
#
#     yaml_file_name = __get_file_name()
#
#     result = []
#
#     if os.path.isfile(yaml_file_name):
#
#         try:
#
#             with open(yaml_file_name, encoding="utf-8-sig") as yaml_file:
#                 result = yaml.safe_load(yaml_file)
#                 if result is None:
#                     result = []
#
#         except yaml.parser.ParserError:
#
#             print(f"Unable to parse: {yaml_file_name}")
#
#     return result
#
#
# def write(logs: list[dict]) -> None:
#     """
#     Writes given logs to the log file.
#     """
#
#     __remove_microseconds(logs)
#
#     yaml_file_name = __get_file_name()
#
#     with open(yaml_file_name, encoding="utf-8-sig", mode="w") as yaml_file:
#         yaml.safe_dump(logs, yaml_file)
#
#
# def __get_file_name() -> str:
#     """
#     Returns a name for the log file.
#     """
#
#     return "timer.yaml"
#
#
# def __remove_microseconds(records: list[dict]):
#     """
#     Removes microseconds from every log.
#     """
#
#     for record in records:
#
#         record["started"] = record["started"].replace(microsecond=0)
#
#         if record.get("stopped") is not None:
#             record["stopped"] = record["stopped"].replace(microsecond=0)


def get_chosen_task(tasks: list) -> parser.Task:

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
