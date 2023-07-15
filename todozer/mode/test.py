import logging

import click
from vkostyanetsky import cliutils

from todozer import scheduler, task_lists, utils
from todozer.todo import list_todo, plan_todo


def main(session: dict) -> None:
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
