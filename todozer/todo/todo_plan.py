from todozer.todo import todo_task


class Plan(todo_task.Task):
    """A single plan class."""

    @property
    def title(self) -> str:
        title = super().title
        index = title.rfind(";")

        if index != -1:
            title = title[:index]

        return title

    @property
    def pattern(self) -> str:
        title = super().title
        index = title.rfind(";")

        next_index = index + 1

        return title[next_index:].strip() if index != -1 else ""
