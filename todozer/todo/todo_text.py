from todozer.todo import todo_item, todo_list, todo_task


class Text(todo_item.Item):
    @staticmethod
    def match(line: str):
        return not todo_list.List.match(line) and not todo_task.Task.match(line)
