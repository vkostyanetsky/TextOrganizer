from todozer import browser, task_lists


def main(session: dict) -> None:
    tasks_file_items = task_lists.load_tasks_file_items(session["config"])
    plans_file_items = task_lists.load_plans_file_items(session["config"])

    browser.TasksBrowser(tasks_file_items, plans_file_items).open()
