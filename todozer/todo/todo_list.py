"""Contains a list class of objects intended to contain tasks to do."""


import datetime
import re

from todozer import constants
from todozer.todo import todo_item, todo_task


class List(todo_item.Item):
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

            match_object = re.match(r"# ([0-9]{4}-[0-9]{2}-[0-9]{2})", self.lines[0])

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
         - 07:30 Bla!

         First item will be the second one after sorting (since 7:30 is earlier
         than 08:00).

         Items without time in the beginning being considering as having 00:00,
         so they are going to move to the very start of the list.
        """

        self.items = sorted(self.items, key=lambda item: item.time)

    def get_active_task(self):
        """
        Returns a task in the list which has a running timer.
        """

        result = None

        for item in self.items:
            if item.is_timer_running():
                result = item
                break

        return result

    def get_scheduled_tasks(self) -> list[todo_task.Task]:
        """
        Returns a list of tasks which are scheduled.
        """

        return list(filter(lambda task: task.is_scheduled, self.items))

    def get_completed_tasks(self) -> list[todo_task.Task]:
        """
        Returns a list of tasks which are completed.
        """

        return list(filter(lambda task: task.is_completed, self.items))
