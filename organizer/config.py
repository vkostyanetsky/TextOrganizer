import os.path as path


def get_tasks_file_path() -> str:
    directory = path.dirname(path.dirname(__file__))
    file_name = "tasks.md"

    return path.join(directory, file_name)


def get_plans_file_path() -> str:
    directory = path.dirname(path.dirname(__file__))
    file_name = "plans.md"

    return path.join(directory, file_name)


def is_date(line: str) -> bool:
    return line.startswith("# ")


def is_task_in_progress(line: str) -> bool:
    return line.startswith("* ")


def is_task_cancelled(line: str) -> bool:
    return line.startswith("- ")


def is_task_completed(line: str) -> bool:
    return line.startswith("+ ")