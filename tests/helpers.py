import datetime

import todozer.utils
from todozer.parser import Plan


def get_plan_ru(pattern: str, start_date: datetime.date = None) -> Plan:
    text = f"* Боб, не стой столбом!; {pattern}"

    if start_date is not None:
        postfix = f" с {todozer.utils.get_string_from_date(start_date)}"
    else:
        postfix = ""

    return Plan(f"{text}{postfix}")


def get_plan_en(pattern: str, start_date: datetime.date = None) -> Plan:
    text = f"* Bob, do something!; {pattern}"

    if start_date is not None:
        postfix = f" from {todozer.utils.get_string_from_date(start_date)}"
    else:
        postfix = ""

    return Plan(f"{text}{postfix}")


def get_day_of_week(day: int) -> datetime.date:
    from_date = datetime.date.today()
    day_index = from_date.weekday()

    different_days = day - day_index if day_index < day else 7 - day_index + day

    return from_date + datetime.timedelta(days=different_days)
