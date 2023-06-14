"""Contains a basic class of items to do."""

import re


class ItemTodo:
    """A basic class of items to do."""

    def __init__(self, line: str) -> None:
        self.lines = [line]

    def __str__(self) -> str:
        """
        Return all the lines of item, separated with line breaks.
        """
        return "\n".join(self.lines)

    @property
    def title_line(self):
        return self.lines[0].strip() if self.lines else ""

    @property
    def title(self) -> str:
        """
        Returns the task's title (first line without markers) (-, +, []).
        """

        return self.title_line.strip()
