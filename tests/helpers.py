import datetime

import todozer.utils
from todozer import constants, utils
from todozer.parser import Plan


def get_debug_code(first_line: str, date: datetime.date) -> str:

    date_string = utils.get_string_from_date(date)
    date_format = constants.DATE_FORMAT

    return f'''
    from todozer import parser
    debug_plan = parser.Plan("{first_line}")
    debug_date = datetime.datetime.strptime("{date_string}", "{date_format}").date()
    print(match(debug_plan, debug_date))'''


def get_plan_ru(pattern: str, start_date: datetime.date = None) -> Plan:
    text = f"- Боб, не стой столбом!; {pattern}"

    if start_date is not None:
        postfix = f" с {todozer.utils.get_string_from_date(start_date)}"
    else:
        postfix = ""

    return Plan(f"{text}{postfix}")


def get_plan_en(pattern: str, start_date: datetime.date = None) -> Plan:
    text = f"- Bob, do something!; {pattern}"

    if start_date is not None:
        postfix = f" from {todozer.utils.get_string_from_date(start_date)}"
    else:
        postfix = ""

    return Plan(f"{text}{postfix}")
