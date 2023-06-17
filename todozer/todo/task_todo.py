import datetime
import re

from todozer.todo import item_todo


class TaskTodo(item_todo.ItemTodo):
    """A single task class."""

    @property
    def title(self) -> str:
        """
        Returns the task's title (first line without markers) (-, +, []).
        """

        result = super().title

        if result.startswith("-"):
            result = result[1:].strip()

        if result.startswith("["):
            regexp = "^(\[.?\])?(.*)"
            groups = re.match(regexp, result)
            result = "" if groups is None else groups[2].strip()

        return result

    @property
    def time(self) -> datetime.time:
        time_string = self.get_time_string()

        return datetime.time.fromisoformat(time_string if time_string else "00:00")

    @property
    def has_time(self) -> bool:
        """
        Returns true if time is specified for this task.
        :return: True of False, depends on time presence
        """
        return len(self.get_time_string()) > 0

    def get_time_string(self) -> str:
        match_object = re.match(r"^([0-9]{1,2}:[0-9]{1,2}).*", self.title)

        return "" if match_object is None else match_object.group(1)

    @staticmethod
    def get_notification_1(line: str) -> dict | None:
        regexp = ".*[notify at|напомнить в] ([0-9]{1,2}):([0-9]{1,2}).*"
        groups = re.match(regexp, line, flags=re.IGNORECASE)

        return (
            None
            if groups is None
            else {
                "time": datetime.time(hour=int(groups[1]), minute=int(groups[2])),
                "repetitions_number": 1,
                "repetitions_period": 0,
            }
        )

    @property
    def notification(self) -> dict | None:
        result = None

        for line in self.lines:
            notification = self.get_notification_1(line)

            if notification is not None:
                result = notification
                break

        return result

    @staticmethod
    def get_time_for_timer() -> str:
        """
        Returns the current hour & minute as a string.
        """

        return datetime.datetime.now().strftime("%H:%M")

    @property
    def timer(self) -> datetime.time:
        seconds = 0
        regexp = r".*(\d{1,2}:\d{1,2}) - (\d{1,2}:\d{1,2})"

        for line in self.lines:
            groups = re.match(regexp, line, flags=re.IGNORECASE)

            if groups is not None:
                date_from = datetime.datetime.strptime(groups[1], "%H:%M")
                date_to = datetime.datetime.strptime(groups[2], "%H:%M")

                seconds += (date_to - date_from).total_seconds()

        hour = round(seconds // 60 // 60)
        seconds -= hour * 60 * 60

        minutes = round(seconds // 60)

        return datetime.time(
            hour=hour if hour >= 0 else 0, minute=minutes if minutes >= 0 else 0
        )

    @property
    def timer_string(self):
        timer = self.timer
        values = []

        if timer.hour > 0:
            values.append(f"{timer.hour}h")

        if timer.minute > 0:
            values.append(f"{timer.minute}m")

        return " ".join(values)

    @property
    def is_scheduled(self) -> bool:
        return (
            TaskTodo.is_scheduled_task(self.lines[0]) if len(self.lines) > 0 else False
        )

    @staticmethod
    def is_scheduled_task(line):
        return line.startswith("- [ ] ")

    @property
    def is_completed(self) -> bool:
        return (
            TaskTodo.is_completed_task(self.lines[0]) if len(self.lines) > 0 else False
        )

    @staticmethod
    def is_completed_task(line):
        return line.startswith("- [x] ")

    @staticmethod
    def match(line: str):
        return TaskTodo.is_scheduled_task(line) or TaskTodo.is_completed_task(line)
