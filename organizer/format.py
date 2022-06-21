from config import *


class TasksFileItem:
    lines: list

    def __init__(self, line: str):
        self.lines = [line]

    def __str__(self):
        return "\n".join(self.lines)


class Separator(TasksFileItem):

    @staticmethod
    def match(line: str):
        return line.startswith("---")


class Header(TasksFileItem):

    @staticmethod
    def match(line: str):
        return line.startswith("# ")


class Task(TasksFileItem):

    @staticmethod
    def match(line: str):
        return is_task_in_progress(line) or is_task_completed(line) or is_task_cancelled(line)


class Text(TasksFileItem):

    @staticmethod
    def match(line: str):
        return not (Separator.match(line) or Header.match(line) or Task.match(line))
