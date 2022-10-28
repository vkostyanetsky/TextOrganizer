#!/usr/bin/env python3

import datetime

import keyboard
from vkostyanetsky import cliutils

from todozer import utils


class TasksBrowser:
    __date: datetime.date

    __tasks: list
    __plans: list

    __previous_day_hotkey: str = "Left"
    __next_day_hotkey: str = "Right"
    __exit_hotkey: str = "Esc"

    def __init__(self, tasks: list, plans: list):

        self.__tasks = tasks
        self.__plans = plans

        self.__date = utils.get_date_of_today()

    def open(self) -> None:

        self.show_log_by_index()

        keyboard.add_hotkey(self.__previous_day_hotkey, self.show_previous_fast)
        keyboard.add_hotkey(self.__next_day_hotkey, self.show_next_fast)

        keyboard.wait(self.__exit_hotkey)

        keyboard.remove_all_hotkeys()

    def show_log_by_index(self):

        cliutils.clear_terminal()

        print()
        print(
            f"Press [{self.__previous_day_hotkey}] and "
            f"[{self.__next_day_hotkey}] to switch logs."
        )
        print(f"Press [{self.__exit_hotkey}] to return to the main menu.")

    def show_previous_fast(self):
        # на дату назад
        self.show_log_by_index()

    def show_next_fast(self):
        if self._index < self._max_index:
            self._index += 1
            self.show_log_by_index()
