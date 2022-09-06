import datetime

import todozer.utils


def get_yesterday_date(today: datetime.date = None) -> datetime.date:

    if today is None:
        today = get_today_date()

    return today - datetime.timedelta(days=1)


def get_today_date() -> datetime.date:
    return datetime.date.today()


def get_tomorrow_date(today: datetime.date = None) -> datetime.date:

    if today is None:
        today = get_today_date()

    return today + datetime.timedelta(days=1)


def get_task_text_ru(pattern: str, start_date: datetime.date = None) -> str:
    text = f"* Боб, не стой столбом!; {pattern}"

    if start_date is not None:
        postfix = f" с {todozer.utils.get_string_from_date(start_date)}"
    else:
        postfix = ""

    return f"{text}{postfix}"


def get_task_text_en(pattern: str, start_date: datetime.date = None) -> str:
    text = f"* Bob, do something!; {pattern}"

    if start_date is not None:
        postfix = f" from {todozer.utils.get_string_from_date(start_date)}"
    else:
        postfix = ""

    return f"{text}{postfix}"
