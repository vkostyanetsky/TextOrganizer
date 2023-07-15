import logging

import click

from todozer import scheduler, task_lists, utils
from todozer.todo import list_todo, plan_todo


def main(path: str = None) -> None:
    """
    Checks plans file for errors.
    """

    config = utils.get_config(path)
    utils.set_logging(config)

    logging.debug("Checking planned tasks...")

    plans_file_items = task_lists.load_plans_file_items(config, path)
    plans_file_issues = []

    __check_plans_file_items(plans_file_items, plans_file_issues)
    __print_report(plans_file_issues)


def __print_report(plans_file_issues) -> None:
    if plans_file_issues:
        click.echo("Issues found in the plans file:")
        click.echo()

        for issue in plans_file_issues:
            click.echo(f"- {issue}")

    else:
        click.echo("Everything seems nice and clear!")

    click.echo()


def __check_plans_file_items(plans_file_items: list, plans_file_issues: list):
    today = utils.get_date_of_today()

    for item in plans_file_items:
        if type(item) == list_todo.ListTodo:
            __check_plans_file_items(item.items, plans_file_issues)

        elif type(item) == plan_todo.PlanTodo:
            matched_pattern, _ = scheduler.match(item, today)

            if matched_pattern == scheduler.Pattern.NONE:
                issue_text = (
                    f'Unable to match pattern for a "{item.title}" plan'
                    f' (pattern text: "{item.pattern}")'
                )

                plans_file_issues.append(issue_text)


if __name__ == "__main__":
    main()
