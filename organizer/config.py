from os.path import dirname, join


def get_tasks_file_path() -> str:
    directory = dirname(dirname(__file__))
    file_name = "tasks.md"

    return join(directory, file_name)


def get_plans_file_path() -> str:
    directory = dirname(dirname(__file__))
    file_name = "plans.md"

    return join(directory, file_name)


def is_date(line: str) -> bool:
    return line.startswith("# ")


def is_task_in_progress(line: str) -> bool:
    return line.startswith("* ")


def is_task_cancelled(line: str) -> bool:
    return line.startswith("- ")


def is_task_completed(line: str) -> bool:
    return line.startswith("+ ")