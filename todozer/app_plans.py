#!/usr/bin/env python3

import logging

from vkostyanetsky import cliutils
from todozer.todo import list_todo, plan_todo
from todozer import app, scheduler, state_file, task_lists, utils
from todozer import constants

def main_menu(session: dict) -> None:
    """
    Displays a submenu to plan tasks.
    """

    menu = cliutils.Menu([constants.TITLE])

    menu.add_item("Create Planned Tasks", create_planned_tasks, session)
    menu.add_item("Health Check", health_check, session)
    menu.add_item("Back", app.main_menu, session)

    menu.choose()


def create_planned_tasks(session: dict) -> None:
    """
    Creates tasks for the today (and days before, in case it was not done yet).

    All tasks in progress must be marked as completed or rearranged
    to other upcoming date before the user runs the procedure.
    """

    logging.debug("Creating planned tasks...")

    tasks_file_items = task_lists.load_tasks_file_items(session["config"])
    plans_file_items = task_lists.load_plans_file_items(session["config"])

    task_lists.add_tasks_lists(tasks_file_items, session["state"]["last_planning_date"])

    if check_for_tasks_in_progress(tasks_file_items):

        filled_list_titles = task_lists.fill_tasks_lists(
            tasks_file_items, plans_file_items, session["state"]
        )

        if filled_list_titles:

            task_lists.save_tasks_file_items(tasks_file_items, session["config"])

            session["state"]["last_planning_date"] = utils.get_date_of_today()
            state_file.save(session["state"])

            scheduled_tasks = ", ".join(filled_list_titles)

            print(f"Tasks for {scheduled_tasks} have been successfully scheduled.")

        else:

            print("Unable to perform, since there are no days to plan tasks.")

        print()

    cliutils.ask_for_enter()

    main_menu(session)


def check_for_tasks_in_progress(tasks_file_items: list) -> bool:

    passed = True

    dates_in_progress = task_lists.get_task_lists_in_progress(tasks_file_items)

    if dates_in_progress:

        passed = False

        print("Unable to perform, since there is at least one task in progress (-):")
        print()

        for date_in_progress in dates_in_progress:
            print(date_in_progress)
            print()

        print("You have to rearrange tasks in progress or mark them as completed (+).")
        print()

    return passed


def health_check(session: dict) -> None:
    """
    Checks plans file for errors.
    """

    logging.debug("Checking planned tasks...")

    plans_file_items = task_lists.load_plans_file_items(session["config"])
    plans_file_issues = []

    check_plans_file_items(plans_file_items, plans_file_issues)

    if plans_file_issues:
        print("Issues found in the plans file:")
        print()

        for issue in plans_file_issues:
            print(f"- {issue}")

    else:
        print("Everything seems nice and clear!")

    print()

    cliutils.ask_for_enter()

    main_menu(session)


def check_plans_file_items(plans_file_items: list, plans_file_issues: list):

    today = utils.get_date_of_today()

    for item in plans_file_items:

        if type(item) == list_todo.ListTodo:

            check_plans_file_items(item.items, plans_file_issues)

        elif type(item) == plan_todo.PlanTodo:

            matched_pattern, _ = scheduler.match(item, today)

            if matched_pattern == scheduler.Pattern.NONE:

                issue_text = (
                    f'Unable to match pattern for a "{item.title}" plan'
                    f' (pattern text: "{item.pattern}")'
                )

                plans_file_issues.append(issue_text)
