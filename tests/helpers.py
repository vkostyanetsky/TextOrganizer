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


def get_day_of_week(day: int) -> datetime.date:
    from_date = datetime.date.today()
    day_index = from_date.weekday()

    different_days = day - day_index if day_index < day else 7 - day_index + day

    return from_date + datetime.timedelta(days=different_days)
