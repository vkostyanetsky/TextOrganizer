from todozer.todo import task_todo


class PlanTodo(task_todo.TaskTodo):
    """A single plan class."""

    @property
    def title(self) -> str:
        result = super().title
        index = result.rfind(";")

        if index != -1:
            result = result[:index]

        return result

    @property
    def pattern(self) -> str:
        title = super().title
        index = title.rfind(";")

        next_index = index + 1

        return title[next_index:].strip() if index != -1 else ""
