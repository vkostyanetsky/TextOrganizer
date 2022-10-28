from todozer.todo import todo_item
import datetime
import re


class Task(todo_item.Item):
    """A single task class."""

    @property
    def time(self) -> datetime.time:

        match_object = re.match("^([0-9]{2}:[0-9]{2}).*", self.title)
        time_string = "00:00" if match_object is None else match_object.group(1)

        return datetime.time.fromisoformat(time_string)

    @staticmethod
    def get_time_for_timer() -> str:
        """
        Returns the current hour & minute as a string.
        """

        return datetime.datetime.now().strftime("%H:%M")

    @staticmethod
    def get_stub_for_timer() -> str:
        """
        Returns string to use instead of ending time string for active timer.
        """

        return "(...)"

    def start_timer(self):
        """
        Adds a mark of an active timer to the task's body.
        """

        time = self.get_time_for_timer()
        stub = self.get_stub_for_timer()

        self.lines.append(f"    {time} -> {stub}")

    def stop_timer(self):
        """
        Replaces a mark of an active timer with an ending time in the task's body.
        """

        line_index = self.get_line_index_with_running_timer()

        if line_index != -1:

            time = self.get_time_for_timer()
            stub = self.get_stub_for_timer()

            self.lines[line_index] = self.lines[line_index].replace(
                stub, time, 1
            )

    def get_line_index_with_running_timer(self) -> int:
        """
        Returns an index of line with a running timer.
        """
        result = -1

        for line_index in range(len(self.lines)):

            if self.lines[line_index].find("(...)") != -1:
                result = line_index
                break

        return result

    def is_timer_running(self):
        return self.get_line_index_with_running_timer() != -1

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
