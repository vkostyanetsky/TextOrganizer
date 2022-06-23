import datetime
import re


class TasksFileItem:
    lines: list

    def __init__(self, line: str):
        self.lines = [line]
        self.items = []

    def __str__(self):
        return "\n".join(self.lines)


class Date(TasksFileItem):
    date_format: str = "%Y-%m-%d"
    date_mark: str = "# "
    items: list

    @staticmethod
    def match(line: str):
        return line.startswith(Date.date_mark)

    @property
    def date(self) -> datetime.date | None:
        result = None

        if len(self.lines[0]) > 0:
            match_object = re.match(r'# ([0-9]{4}-[0-9]{2}-[0-9]{2})', self.lines[0])

            if match_object is not None:
                string = match_object.group(1)
                result = datetime.datetime.strptime(string, Date.date_format).date()

        return result


class Task(TasksFileItem):
    scheduled_task_mark: str = "* "
    completed_task_mark: str = "+ "
    cancelled_task_mark: str = "- "

    @staticmethod
    def is_scheduled_task(line):
        return line.startswith(Task.scheduled_task_mark)

    @staticmethod
    def is_completed_task(line):
        return line.startswith(Task.completed_task_mark)

    @staticmethod
    def is_cancelled_task(line):
        return line.startswith(Task.cancelled_task_mark)

    @staticmethod
    def match(line: str):
        return Task.is_scheduled_task(line) or Task.is_completed_task(line) or Task.is_cancelled_task(line)


class Text(TasksFileItem):

    @staticmethod
    def match(line: str):
        return not Date.match(line) and not Task.match(line)
