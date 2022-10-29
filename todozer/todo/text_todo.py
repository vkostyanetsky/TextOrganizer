from todozer.todo import item_todo, list_todo, task_todo


class TextTodo(item_todo.ItemTodo):
    @staticmethod
    def match(line: str):
        return not list_todo.ListTodo.match(line) and not task_todo.TaskTodo.match(line)
