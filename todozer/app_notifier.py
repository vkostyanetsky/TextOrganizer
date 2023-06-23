import datetime
import logging
import time

import requests
from vkostyanetsky import cliutils

from todozer import state_file, task_lists, utils
from todozer.todo import list_todo


def main(session: dict) -> None:
    """
    Starts the everlasting loop of notifying.
    :param session: user's session data
    :return: nothing
    """

    logging.debug("Notifier is starting...")

    last_planned_date = session["state"]["last_planning_date"]

    while True:
        notifications_today = []

        tasks_file_items = task_lists.load_tasks_file_items(session["config"])
        plans_file_items = task_lists.load_plans_file_items(session["config"])

        date = last_planned_date

        future_days_number = int(
            session["config"].get("NOTIFICATIONS", "future_days_number")
        )

        for _ in range(future_days_number):
            tasks_group = task_lists.get_tasks_list_by_date(tasks_file_items, date)

            if tasks_group is None:
                tasks_group = list_todo.ListTodo(
                    f"# {utils.get_string_from_date(date)}"
                )

            if date > last_planned_date:
                task_lists.fill_tasks_list(tasks_group, plans_file_items)

            for task in tasks_group.items:
                if task.is_scheduled and task.notifications:
                    for notification in task.notifications:
                        remind_at = datetime.datetime(
                            year=tasks_group.date.year,
                            month=tasks_group.date.month,
                            day=tasks_group.date.day,
                            hour=notification["time"].hour,
                            minute=notification["time"].minute,
                            second=0,
                        )

                        if datetime.datetime.now() >= remind_at:
                            __notify(date, task, notification["time"], session)
                        elif date == datetime.date.today():
                            notifications_today.append(
                                {"time": notification["time"], "title": task.title}
                            )

            date += datetime.timedelta(days=1)

        state_file.save(session["state"])

        cliutils.clear_terminal()

        print(
            f"TODAY'S NOTIFICATIONS AS OF {datetime.datetime.now().strftime('%H:%M')}"
        )
        print()

        if notifications_today:
            notifications_today = sorted(
                notifications_today,
                key=lambda item: item["time"],
            )

            for task in notifications_today:
                print(f"🔔 {task['time']:%H:%M} | {task['title']}")
        else:
            print("No notifications found.")

        __wait_for_next_minute()


def __notify(date, task, notification_time, session) -> None:
    date_string = utils.get_string_from_date(date)
    time_string = notification_time.strftime("%H:%M")

    triggered_notifications = session["state"].get("triggered_notifications")

    if triggered_notifications.get(date_string) is None:
        triggered_notifications[date_string] = {}

    if triggered_notifications[date_string].get(task.title_line) is None:
        triggered_notifications[date_string][task.title_line] = []

    if time_string not in triggered_notifications[date_string][task.title_line]:
        __send_to_telegram_chat(task.title, session["config"])
        triggered_notifications[date_string][task.title_line].append(time_string)


def __wait_for_next_minute() -> None:
    logging.debug(f"Waiting for the next minute...")

    time.sleep(60 - datetime.datetime.now().second)


def __send_to_telegram_chat(text: str, config: dict) -> None:
    bot_api_token = config.get("NOTIFICATIONS", "telegram_bot_api_token")
    chat_id = config.get("NOTIFICATIONS", "telegram_chat_id")

    try:
        url = f"https://api.telegram.org/bot{bot_api_token}/sendMessage"

        data = {
            "parse_mode": "HTML",
            "chat_id": chat_id,
            "text": f"{text}",
        }

        response = requests.post(url, params=data)

        if response.status_code != 200:
            raise Exception(response.text)

    except Exception as error:
        logging.error(f"Error while sending a message to Telegram: {error}")


def __tasks_for_today(
    items: list, last_planned_date: datetime.date
) -> list_todo.ListTodo | None:
    result = None

    index = -1

    while index >= -len(items):
        item = items[index]

        if item.date == last_planned_date:
            result = index
            break

        index -= 1

    return result
