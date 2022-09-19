import datetime

from todozer import parser, scheduler, utils


def add_tasks_lists(tasks: list, last_date: datetime.date):

    date = utils.get_date_of_tomorrow(last_date)
    today = utils.get_date_of_today()

    while date <= today:

        task_lists_by_date = filter(
            lambda item: type(item) is parser.List and item.date == date, tasks
        )  # TODO probably better to do it like .is_date (duck typing)

        if not list(task_lists_by_date):

            date_string = utils.get_string_from_date(date)
            line = f"# {date_string}"
            tasks.append(parser.List(line))

        date = utils.get_date_of_tomorrow(date)


def fill_tasks_lists(task_items: list, plan_items: list, data: dict) -> list:

    filled_list_titles = []

    today = utils.get_date_of_today()

    for task_item in task_items:

        is_list_to_fill = (
            type(task_item) == parser.List
            and task_item.date is not None
            and data["last_date"] < task_item.date <= today
        )

        if is_list_to_fill:
            fill_tasks_list(task_item, plan_items)
            sort_tasks_list(task_item)

            filled_list_titles.append(task_item.title)

    return filled_list_titles


def sort_tasks_list(tasks_file_item: parser.List):

    tasks_file_item.items = sorted(tasks_file_item.items, key=lambda item: item.time)


def fill_tasks_list(tasks_file_item: parser.List, plans_file_items: list):

    for plans_file_item in plans_file_items:

        if isinstance(plans_file_item, parser.List):

            fill_tasks_list(tasks_file_item, plans_file_item.items)

        elif isinstance(plans_file_item, parser.Plan):

            _, is_date_matched = scheduler.match(plans_file_item, tasks_file_item.date)

            if is_date_matched:

                line = f"- {plans_file_item.title}"
                task = parser.Task(line)

                if len(plans_file_item.lines) > 1:

                    i = 0

                    for plan_line in plans_file_item.lines:

                        i += 1

                        if i == 1:
                            continue

                        task.lines.append(plan_line)

                tasks_file_item.items.append(task)


def get_task_lists_in_progress(file_items: list) -> list:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    dates_in_progress = []

    for file_item in file_items:

        if type(file_item) == parser.List and file_item.date <= yesterday:

            scheduled_tasks = file_item.get_scheduled_tasks()

            if scheduled_tasks:
                incomplete_day = parser.List(file_item.lines[0])
                incomplete_day.items = scheduled_tasks

                dates_in_progress.append(incomplete_day)

    return dates_in_progress
