"""Contains a list class of objects intended to contain tasks to do."""


import datetime
import re

from todozer import constants
from todozer.todo import item_todo, task_todo


class ListTodo(item_todo.ItemTodo):
    """Tasks collection class."""

    def __init__(self, line: str):
        super().__init__(line)
        self.items = []

    def __str__(self) -> str:
        """
        Returns all the lines of the item (its own title in most cases),
        and all the lines of tasks inside it.
        """

        lines = super().__str__()
        items = "\n".join(list(map(str, self.items)))

        return f"{lines}\n\n{items}"

    @property
    def title(self) -> str:
        """
        Returns the list's title.
        """

        result = self.title_line.strip()

        if result.startswith("#"):
            result = result[1:].strip()

        return result

    @staticmethod
    def match(line: str):
        """
        Returns True if the string given looks like a list header.
        """

        return line.startswith("# ")

    @property
    def date(self) -> datetime.date | None:
        """
        Return a date of the list, if it is possible to determine using the ISO standard.
        """

        result = None

        if self.lines[0]:
            match_object = re.match(r"# ([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})", self.lines[0])

            if match_object is not None:
                string = match_object.group(1)
                result = datetime.datetime.strptime(
                    string, constants.DATE_FORMAT
                ).date()

        return result

    def sort_tasks(self):
        """
        Sorts tasks by their time.

        For instance:

        - 08:00 Bla bla bla!
        - Buy a cup of coffee
        - 07:30 Bla!

        After sorting:

        - 07:30 Bla!
        - 08:00 Bla bla bla!
        - Buy a cup of coffee

        Pay attention that tasks without time specified come last.
        """

        self.items = sorted(
            self.items,
            key=lambda item: datetime.time(hour=23, minute=59, second=59)
            if not item.has_time
            else item.time,
        )

    def get_scheduled_tasks(self) -> list[task_todo.TaskTodo]:
        """
        Returns a list of tasks which are scheduled.
        """

        return list(filter(lambda task: task.is_scheduled, self.items))

    def get_completed_tasks(self) -> list[task_todo.TaskTodo]:
        """
        Returns a list of tasks which are completed.
        """

        return list(filter(lambda task: task.is_completed, self.items))
