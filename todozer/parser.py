#!/usr/bin/env python3

import datetime
import re

from todozer import constants


class Item:
    """A base class for tasks file item."""

    def __init__(self, line: str):
        self.lines = [line]

    def __str__(self) -> str:
        return "\n".join(self.lines)

    @property
    def first_line(self) -> str:
        return self.lines[0] if self.lines else ""

    @property
    def title(self):
        first_line = self.first_line

        return first_line[1:].strip() if first_line else ""


class List(Item):
    """Tasks collection class."""

    def __init__(self, line: str):
        super().__init__(line)
        self.items = []

    def __str__(self) -> str:
        lines = super().__str__()
        items = "\n".join(list(map(lambda item: str(item), self.items)))

        return f"{lines}\n\n{items}"

    def get_tasks(self) -> list:
        filter_result = filter(lambda item: type(item) == Task, self.items)

        return list(filter_result)

    def get_scheduled_tasks(self) -> list:
        tasks = self.get_tasks()
        filter_result = filter(lambda task: task.is_scheduled, tasks)

        return list(filter_result)

    def get_completed_tasks(self) -> list:
        tasks = self.get_tasks()
        filter_result = filter(lambda task: task.is_completed, tasks)

        return list(filter_result)

    @property
    def date(self) -> datetime.date | None:
        result = None

        if self.lines[0]:
            match_object = re.match(r"# ([0-9]{4}-[0-9]{2}-[0-9]{2})", self.lines[0])

            if match_object is not None:
                string = match_object.group(1)
                result = datetime.datetime.strptime(
                    string, constants.DATE_FORMAT
                ).date()

        return result

    @staticmethod
    def match(line: str):
        return line.startswith("# ")


class Task(Item):
    """A single task class."""

    @property
    def time(self) -> datetime.time:

        match_object = re.match("^([0-9]{2}:[0-9]{2}).*", self.title)
        time_string = "00:00" if match_object is None else match_object.group(1)

        return datetime.time.fromisoformat(time_string)

    @property
    def is_scheduled(self) -> bool:
        return Task.is_scheduled_task(self.lines[0]) if len(self.lines) > 0 else False

    @staticmethod
    def is_scheduled_task(line):
        return line.startswith("- ")

    @property
    def is_completed(self) -> bool:
        return Task.is_completed_task(self.lines[0]) if len(self.lines) > 0 else False

    @staticmethod
    def is_completed_task(line):
        return line.startswith("+ ")

    @staticmethod
    def match(line: str):
        return Task.is_scheduled_task(line) or Task.is_completed_task(line)


class Text(Item):  # TODO probably deprecated
    @staticmethod
    def match(line: str):
        return not List.match(line) and not Task.match(line)


class Plan(Task):
    """A single plan class."""

    @property
    def title(self) -> str:
        title = super().title
        index = title.rfind(";")

        if index != -1:
            title = title[:index]

        return title

    @property
    def pattern(self) -> str:
        title = super().title
        index = title.rfind(";")

        next_index = index + 1

        return title[next_index:].strip() if index != -1 else ""


class Parser:
    __file_path: str = ""
    __last_list: List | None
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

                if List.match(line):
                    self.__add_date(line)
                elif self.__task_class.match(line):
                    self.__add_task(line)
                elif line.strip() != "":
                    self.__add_text(line)

        return self.__file_items

    def __add_date(self, line: str):
        self.__add_empty_lines_to_last_date()

        new_item = List(line)

        self.__file_items.append(new_item)
        self.__last_list = new_item

    def __add_task(self, line: str):
        self.__add_empty_lines_to_last_date()

        if self.__last_list is None:
            self.__file_items.append(Text(line))
        else:
            self.__last_list.items.append(self.__task_class(line))

    def __add_text(self, line: str):

        previous_task = self.__get_previous_task()

        if previous_task is not None:

            self.__add_empty_lines(previous_task.lines)

            previous_task.lines.append(line)

        else:

            new_item = Text(line)

            if self.__last_list is not None:

                self.__add_empty_lines(self.__last_list.items)

                self.__last_list.items.append(new_item)

            else:

                self.__add_empty_lines(self.__file_items)

                self.__file_items.append(new_item)

    def __get_previous_task(self) -> Task | Plan | None:
        previous_task = None

        if self.__file_items:

            last_file_item = self.__file_items[-1]

            if type(last_file_item) == List:

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
            new_item = Text(empty_line)
            collection.append(new_item)

        self.__empty_lines.clear()
