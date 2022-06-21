from config import *


class TasksFileItem:
    date: None
    lines: list

    def __init__(self, line: str):
        self.lines = [line]

    def __str__(self):
        return "\n".join(self.lines)


class Date(TasksFileItem):

    @staticmethod
    def match(line: str):
        return is_date(line)


class Task(TasksFileItem):

    @staticmethod
    def match(line: str):
        return is_task_in_progress(line) or is_task_completed(line) or is_task_cancelled(line)


class Text(TasksFileItem):

    @staticmethod
    def match(line: str):
        return not Date.match(line) and not Task.match(line)
