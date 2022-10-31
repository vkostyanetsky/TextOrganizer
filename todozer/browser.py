#!/usr/bin/env python3

import datetime

import keyboard
from vkostyanetsky import cliutils

from todozer import task_lists, utils
from todozer.todo import list_todo


class TasksBrowser:
    __date: datetime.date

    __tasks: list
    __plans: list
    __planned_dates: list

    __previous_day_hotkey: str = "Left"
    __next_day_hotkey: str = "Right"
    __exit_hotkey: str = "Esc"

    def __init__(self, tasks: list, plans: list):

        self.__tasks = tasks
        self.__plans = plans

        self.__planned_dates = []

        self.__date = utils.get_date_of_today()

    def open(self) -> None:

        self.show_tasks_by_date()

        keyboard.add_hotkey(self.__previous_day_hotkey, self.show_previous_fast)
        keyboard.add_hotkey(self.__next_day_hotkey, self.show_next_fast)

        keyboard.wait(self.__exit_hotkey)

        keyboard.remove_all_hotkeys()

    def show_tasks_by_date(self):

        cliutils.clear_terminal()

        title = utils.get_string_from_date(self.__date)

        print(f"# {title}")
        print()

        tasks_list = task_lists.get_tasks_list_by_date(self.__tasks, self.__date)

        if tasks_list is None:
            self.__tasks.append(list_todo.ListTodo(f"# {title}"))
            tasks_list = self.__tasks[-1]

        if self.__date > utils.get_date_of_today():

            if self.__date not in self.__planned_dates:
                task_lists.fill_tasks_list(tasks_list, self.__plans)
                self.__planned_dates.append(self.__date)

        if tasks_list.items:

            for task in tasks_list.items:
                timer_string = task.timer_string
                if timer_string != "":
                    timer_string = f" ({timer_string})"

                print(f"{task.title_line}{timer_string}")

        else:

            print("No tasks found.")

        print()
        print(
            f"Press [{self.__previous_day_hotkey}] and "
            f"[{self.__next_day_hotkey}] to switch logs."
        )
        print(f"Press [{self.__exit_hotkey}] to return to the main menu.")

    def show_previous_fast(self):
        self.__date -= datetime.timedelta(days=1)
        self.show_tasks_by_date()

    def show_next_fast(self):
        self.__date += datetime.timedelta(days=1)
        self.show_tasks_by_date()
