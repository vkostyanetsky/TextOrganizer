import datetime
import re


class Item:
    lines: list

    def __init__(self, line: str):
        self.lines = [line]

    def __str__(self) -> str:
        return "\n".join(self.lines)

    @property
    def title(self) -> str:
        return self.lines[0] if len(self.lines) > 0 else ''


class Date(Item):
    date_format: str = "%Y-%m-%d"
    date_mark: str = "# "
    items: list

    def __init__(self, line: str):
        super().__init__(line)
        self.items = []

    def __str__(self) -> str:
        lines = super().__str__()
        items = "\n".join(list(map(lambda item: str(item), self.items)))

        return f"{lines}\n{items}"

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

    def get_cancelled_tasks(self) -> list:
        tasks = self.get_tasks()
        filter_result = filter(lambda task: task.is_cancelled, tasks)

        return list(filter_result)

    @property
    def date(self) -> datetime.date | None:
        result = None

        if len(self.lines[0]) > 0:
            match_object = re.match(r"# ([0-9]{4}-[0-9]{2}-[0-9]{2})", self.lines[0])

            if match_object is not None:
                string = match_object.group(1)
                result = datetime.datetime.strptime(string, Date.date_format).date()

        return result

    @staticmethod
    def match(line: str):
        return line.startswith(Date.date_mark)


class Plan(Item):
    def get_pattern(self):
        result = ""
        source = self.lines[0]

        index = source.rfind(";")

        if index != -1:
            index += 1
            result = source[index:].strip()

        return result


class Task(Item):
    scheduled_task_mark: str = "* "
    completed_task_mark: str = "+ "
    cancelled_task_mark: str = "- "

    @property
    def is_scheduled(self) -> bool:
        return Task.is_scheduled_task(self.lines[0]) if len(self.lines) > 0 else False

    @staticmethod
    def is_scheduled_task(line):
        return line.startswith(Task.scheduled_task_mark)

    @property
    def is_completed(self) -> bool:
        return Task.is_completed_task(self.lines[0]) if len(self.lines) > 0 else False

    @staticmethod
    def is_completed_task(line):
        return line.startswith(Task.completed_task_mark)

    @property
    def is_cancelled(self) -> bool:
        return Task.is_cancelled_task(self.lines[0]) if len(self.lines) > 0 else False

    @staticmethod
    def is_cancelled_task(line):
        return line.startswith(Task.cancelled_task_mark)

    @staticmethod
    def match(line: str):
        return (
            Task.is_scheduled_task(line)
            or Task.is_completed_task(line)
            or Task.is_cancelled_task(line)
        )


class Text(Item):
    @staticmethod
    def match(line: str):
        return not Date.match(line) and not Task.match(line)


class Parser:
    __file_path: str = ""
    __last_date: Date | None
    __file_items: list = []
    __empty_lines: list = []

    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__last_date = None
        self.__file_items = []
        self.__empty_lines = []

    def parse(self) -> list:

        tasks_file = open(self.__file_path, "r", encoding="utf-8-sig")

        with tasks_file:

            while True:

                line = tasks_file.readline()

                if not line:
                    break

                line = line.rstrip("\n")

                if Date.match(line):
                    self.__add_date(line)
                elif Task.match(line):
                    self.__add_task(line)
                else:
                    self.__add_text(line)

        return self.__file_items

    def __add_date(self, line: str):
        self.__add_empty_lines_to_last_date()

        new_item = Date(line)

        self.__file_items.append(new_item)
        self.__last_date = new_item

    def __add_task(self, line: str):
        self.__add_empty_lines_to_last_date()

        if self.__last_date is None:
            self.__file_items.append(Text(line))
        else:
            self.__last_date.items.append(Task(line))

    def __add_text(self, line: str):
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
        self.__add_empty_lines(
            self.__file_items if self.__last_date is None else self.__last_date.items
        )

    def __add_empty_lines(self, collection) -> None:
        for empty_line in self.__empty_lines:
            new_item = Text(empty_line)
            collection.append(new_item)

        self.__empty_lines.clear()
