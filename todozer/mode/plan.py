import logging

from vkostyanetsky import cliutils

from todozer import state_file, task_lists, utils


def main(session: dict) -> None:
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

            __clean_triggered_notifications(session)

            state_file.save(session["state"])

            scheduled_tasks = ", ".join(filled_list_titles)

            print(f"Tasks for {scheduled_tasks} have been successfully scheduled.")

        else:
            print("Unable to perform, since there are no days to plan tasks.")

        print()

    cliutils.ask_for_enter()


def check_for_tasks_in_progress(tasks_file_items: list) -> bool:
    passed = True

    dates_in_progress = task_lists.get_task_lists_in_progress(tasks_file_items)

    if dates_in_progress:
        passed = False

        print("Unable to perform, since there is at least one task in progress:")
        print()

        for date_in_progress in dates_in_progress:
            print(date_in_progress)
            print()

        print("You have to rearrange tasks in progress or mark them as completed.")
        print()

    return passed


def __clean_triggered_notifications(session: dict) -> None:
    date_strings = list(session["state"]["triggered_notifications"].keys())

    for date_string in date_strings:
        if (
            utils.get_date_from_string(date_string)
            < session["state"]["last_planning_date"]
        ):
            del session["state"]["triggered_notifications"][date_string]
