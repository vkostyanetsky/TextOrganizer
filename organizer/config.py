def get_tasks_file_name() -> str:
    return "tasks.md"


def get_plans_file_name() -> str:
    return "plans.md"


def is_task_in_progress(line: str) -> bool:
    return line.startswith("* ")


def is_task_cancelled(line: str) -> bool:
    return line.startswith("- ")


def is_task_completed(line: str) -> bool:
    return line.startswith("+ ")