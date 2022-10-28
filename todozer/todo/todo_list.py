from todozer.todo import todo_item, todo_task
import re
import datetime
from todozer import constants


class List(todo_item.Item):
    """Tasks collection class."""

    def __init__(self, line: str):
        super().__init__(line)
        self.items = []

    def __str__(self) -> str:
        lines = super().__str__()
        items = "\n".join(list(map(lambda item: str(item), self.items)))

        return f"{lines}\n\n{items}"

    def get_tasks(self) -> list:
        filter_result = filter(lambda item: type(item) == todo_task.Task, self.items)

        return list(filter_result)

    def get_scheduled_tasks(self) -> list:
        tasks = self.get_tasks()
        filter_result = filter(lambda task: task.is_scheduled, tasks)

        return list(filter_result)

    def get_completed_tasks(self) -> list:
        tasks = self.get_tasks()
        filter_result = filter(lambda task: task.is_completed, tasks)

        return list(filter_result)

    def sort_items(self):
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
        result = None
        for item in self.items:
            if item.is_timer_running():
                result = item
                break
        return result

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
