#!/usr/bin/env python3

from vkostyanetsky import cliutils

from todozer import app, browser, task_lists


def main_menu(session: dict) -> None:
    tasks_file_items = task_lists.load_tasks_file_items(session["config"])
    plans_file_items = task_lists.load_plans_file_items(session["config"])

    browser.TasksBrowser(tasks_file_items, plans_file_items).open()

    app.main_menu(session)
