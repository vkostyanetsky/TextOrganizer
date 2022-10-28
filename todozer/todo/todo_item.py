class Item:
    """A base class for tasks file item."""

    def __init__(self, line: str):
        self.lines = [line]

    def __str__(self) -> str:
        return "\n".join(self.lines)

    @property
    def first_line(self) -> str:
        return self.lines[0] if self.lines else ""

    @property
    def title(self):
        first_line = self.first_line

        return first_line[1:].strip() if first_line else ""
