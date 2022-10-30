#!/usr/bin/env python3

from todozer import constants
from todozer.todo import list_todo, plan_todo, task_todo, text_todo


class Parser:
    __file_path: str = ""
    __last_list: list_todo.ListTodo | None
    __file_items: list = []
    __task_class = None
    __empty_lines: list = []

    def __init__(self, file_path: str, task_class):
        self.__file_path = file_path
        self.__last_list = None
        self.__file_items = []
        self.__task_class = task_class
        self.__empty_lines = []

    def parse(self) -> list:

        tasks_file = open(self.__file_path, "r", encoding=constants.ENCODING)

        with tasks_file:

            while True:

                line = tasks_file.readline()

                if not line:
                    break

                line = line.rstrip("\n")

                if list_todo.ListTodo.match(line):
                    self.__add_date(line)
                elif self.__task_class.match(line):
                    self.__add_task(line)
                elif line.strip() != "":
                    self.__add_text(line)

        return self.__file_items

    def __add_date(self, line: str):
        self.__add_empty_lines_to_last_date()

        new_item = list_todo.ListTodo(line)

        self.__file_items.append(new_item)
        self.__last_list = new_item

    def __add_task(self, line: str):
        self.__add_empty_lines_to_last_date()

        if self.__last_list is None:
            self.__file_items.append(text_todo.TextTodo(line))
        else:
            self.__last_list.items.append(self.__task_class(line))

    def __add_text(self, line: str):

        previous_task = self.__get_previous_task()

        if previous_task is not None:

            self.__add_empty_lines(previous_task.lines)

            previous_task.lines.append(line)

        else:

            new_item = text_todo.TextTodo(line)

            if self.__last_list is not None:

                self.__add_empty_lines(self.__last_list.items)

                self.__last_list.items.append(new_item)

            else:

                self.__add_empty_lines(self.__file_items)

                self.__file_items.append(new_item)

    def __get_previous_task(self) -> task_todo.TaskTodo | plan_todo.PlanTodo | None:
        previous_task = None

        if self.__file_items:

            last_file_item = self.__file_items[-1]

            if type(last_file_item) == list_todo.ListTodo:

                if last_file_item.items:

                    if type(last_file_item.items[-1]) == self.__task_class:
                        previous_task = last_file_item.items[-1]

            elif type(last_file_item) == self.__task_class:
                previous_task = last_file_item

        return previous_task

    def __add_empty_lines_to_last_date(self) -> None:

        self.__add_empty_lines(
            self.__file_items if self.__last_list is None else self.__last_list.items
        )

    def __add_empty_lines(self, collection) -> None:
        for empty_line in self.__empty_lines:
            new_item = text_todo.TextTodo(empty_line)
            collection.append(new_item)

        self.__empty_lines.clear()
