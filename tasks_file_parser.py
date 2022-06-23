from tasks_file_format import *


class TasksFileParser:
    __file_path: str = ""
    __last_date: Date | None
    __file_items: list = []
    __empty_lines: list = []

    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__last_date = None
        self.__file_items = []

    def parse(self) -> list:

        tasks_file = open(self.__file_path, "r", encoding="utf-8-sig")

        with tasks_file:

            while True:

                line = tasks_file.readline()

                if not line:
                    break

                if Date.match(line):

                    self.__add_date(line)

                elif Task.match(line):

                    self.__add_task(line)

                else:

                    if line.strip() == "":

                        self.__empty_lines.append(line)

                    else:

                        previous_task = self.__get_previous_task()

                        if previous_task is not None:

                            self.__add_empty_lines(previous_task.lines)

                            previous_task.lines.append(line)

                        else:

                            new_item = Text(line)

                            if self.__last_date is not None:

                                self.__add_empty_lines(self.__last_date.items)

                                self.__last_date.items.append(new_item)

                            else:

                                self.__add_empty_lines(self.__file_items)

                                self.__file_items.append(new_item)

        return self.__file_items

    def __add_date(self, line: str):
        self.__add_empty_lines_to_last_date()

        new_item = Date(line)

        self.__file_items.append(new_item)
        self.__last_date = new_item

    def __add_task(self, line: str):
        self.__add_empty_lines_to_last_date()

        new_item = Task(line)

        if self.__last_date is None:
            self.__file_items.append(new_item)
        else:
            self.__last_date.items.append(new_item)

    def __get_previous_task(self) -> Task | None:
        previous_task = None

        if len(self.__file_items) > 0:

            last_file_item = self.__file_items[-1]

            if type(last_file_item) == Date:

                if len(last_file_item.items) > 0:

                    if type(last_file_item.items[-1]) == Task:
                        previous_task = last_file_item.items[-1]

            elif type(last_file_item) == Task:
                previous_task = last_file_item

        return previous_task

    def __add_empty_lines_to_last_date(self) -> None:
        self.__add_empty_lines(self.__file_items if self.__last_date is None else self.__last_date.items)

    def __add_empty_lines(self, collection) -> None:
        for empty_line in self.__empty_lines:

            new_item = Text(empty_line)
            collection.append(new_item)

        self.__empty_lines.clear()
