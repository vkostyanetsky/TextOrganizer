import datetime
import logging
import re
from enum import Enum, auto

from todozer import utils
from todozer.parser import Plan


class Pattern(Enum):
    """Task repetition patterns."""

    EXACT_DATE = auto()
    EVERY_DAY = auto()
    EVERY_N_DAY = auto()
    EVERY_MONTH = auto()
    EVERY_WEEKDAY = auto()
    EVERY_YEAR = auto()
    EVERY_MONDAY = auto()
    EVERY_TUESDAY = auto()
    EVERY_WEDNESDAY = auto()
    EVERY_THURSDAY = auto()
    EVERY_FRIDAY = auto()
    EVERY_SATURDAY = auto()
    EVERY_SUNDAY = auto()


def match(plan: Plan, date: datetime.date) -> Pattern | None:

    logging.debug(
        f'Attempt to plan "{str(plan)}" on {utils.get_string_from_date(date)}'
    )

    matched = None

    if plan.pattern == "":
        logging.debug("Pattern to plan is not found.")
    else:
        logging.debug("Pattern to plan: %s", plan.pattern)

        matched = match_pattern(plan.pattern, date)

    return matched


def match_pattern(pattern: str, date: datetime.date) -> Pattern | None:

    matched = None

    compiled_pattern = get_compiled_pattern(pattern)

    logging.debug("Compiled pattern: %s", compiled_pattern)

    readers = {
        Pattern.EXACT_DATE: pattern_exact_date,
        Pattern.EVERY_DAY: pattern_every_day,
        Pattern.EVERY_N_DAY: pattern_every_n_day,
        Pattern.EVERY_MONTH: pattern_every_month,
        Pattern.EVERY_WEEKDAY: pattern_every_weekday,
        Pattern.EVERY_YEAR: pattern_every_year,
        Pattern.EVERY_MONDAY: pattern_every_monday,
        Pattern.EVERY_TUESDAY: pattern_every_tuesday,
        Pattern.EVERY_WEDNESDAY: pattern_every_wednesday,
        Pattern.EVERY_THURSDAY: pattern_every_thursday,
        Pattern.EVERY_FRIDAY: pattern_every_friday,
        Pattern.EVERY_SATURDAY: pattern_every_saturday,
        Pattern.EVERY_SUNDAY: pattern_every_sunday,
    }

    logging.debug("Matching the pattern...")

    for reader in readers:

        function = readers[reader]

        logging.debug('Checking a reader: "%s"...', function.__name__)

        if function(compiled_pattern, date):
            matched = reader
            break

    logging.debug(f"Matched pattern: {matched}")

    return matched


def get_compiled_pattern(text: str) -> str:

    rules = [
        (" с ", " from "),
        ("по будням|по будним дням", "every weekday"),
        ("будний день", "weekday"),
        ("день", "day"),
        ("месяц", "month"),
        ("год", "year"),
        ("дня|дней", "days"),
        ("последний", "last"),
        ("каждый|каждая|каждое|каждую|каждые", "every"),
        ("январь|января|january", "jan"),
        ("февраль|февраля|february", "feb"),
        ("март|марта|march", "mar"),
        ("апрель|апреля|april", "apr"),
        ("май|мая|may", "may"),
        ("июнь|июня|june", "jun"),
        ("июль|июля|july", "jul"),
        ("август|августа|august", "aug"),
        ("сентябрь|сентября|september", "sep"),
        ("октябрь|октября|october", "oct"),
        ("ноябрь|ноября|november", "nov"),
        ("декабрь|декабря|december", "dec"),
        ("понедельник", "monday"),
        ("вторник", "tuesday"),
        ("среда|среду", "wednesday"),
        ("четверг", "thursday"),
        ("пятница|пятницу", "friday"),
        ("суббота|субботу", "saturday"),
        ("воскресенье", "sunday"),
    ]

    for rule in rules:

        source_regexp = rf"(.*)({rule[0]})(.*)"
        result_regexp = rf"\1{rule[1]}\3"

        text = re.sub(source_regexp, result_regexp, text, flags=re.IGNORECASE)

    return text.strip()


def pattern_exact_date(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - 1983-12-29
    """

    date_regexp = get_regexp_for_date()
    full_regexp = f"({date_regexp}).*"

    result = False
    groups = re.match(full_regexp, text)

    if groups is not None:
        result = date == utils.get_date_from_string(groups[1])

    return result


def pattern_every_day(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждый день
    - every day
    """
    result = False

    if match_pattern_title(text, "every day.*"):
        result = match_pattern_start_date(text, date)

    return result


def pattern_every_n_day(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждый 1 день
    - каждые 2 дня
    - каждые 5 дней
    - every 1 day
    - every 3 days
    """

    result = False

    regexp = ".*every ([0-9]+) (day|days).*"
    groups = re.match(regexp, text)

    if groups is not None:

        day_number = int(groups[1])
        start_date = get_start_date(text)

        if start_date is not None and date >= start_date:
            result = abs(date - start_date).days % day_number == 0

    return result


def pattern_every_monday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждый понедельник
    - каждый пн
    - every monday
    - every mon
    """

    return match_pattern_title_and_day_name_for_date(text, date, "every monday", "Mon")


def pattern_every_tuesday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждый вторник
    - каждый вт
    - every tuesday
    - every tue
    """

    return match_pattern_title_and_day_name_for_date(text, date, "every tuesday", "Tue")


def pattern_every_wednesday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждую среду
    - каждую ср
    - every wednesday
    - every wed
    """

    return match_pattern_title_and_day_name_for_date(
        text, date, "every wednesday", "Wed"
    )


def pattern_every_thursday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждый четверг
    - каждый чт
    - every thursday
    - every thu
    """

    return match_pattern_title_and_day_name_for_date(
        text, date, "every thursday", "Thu"
    )


def pattern_every_friday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждую пятницу
    - каждую пт
    - every friday
    - every fri
    """

    return match_pattern_title_and_day_name_for_date(text, date, "every friday", "Fri")


def pattern_every_saturday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждую субботу
    - каждую сб
    - every sat
    """

    return match_pattern_title_and_day_name_for_date(
        text, date, "every saturday", "Sat"
    )


def pattern_every_sunday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждое воскресенье
    - каждое вс
    - every sun
    """

    return match_pattern_title_and_day_name_for_date(text, date, "every sunday", "Sun")


def pattern_every_weekday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - по будням
    - по будним дням
    - каждый будний день
    - weekdays
    - every weekday
    """

    result = False

    regexp = "(weekdays|every weekday).*"
    groups = re.match(regexp, text)

    if groups is not None and 0 <= date.weekday() <= 4:
        result = match_pattern_start_date(text, date)

    return result


def pattern_every_month(text: str, date: datetime.date) -> bool:
    """
    каждый месяц, 5 день
    каждый месяц, последний день

    каждый месяц, 5 день, начиная с 29.12.1983
    каждый месяц, 5 день с 29.12.1983

    :param text: text to match
    :param date: date to match
    :return: matched or not
    """

    result = False
    regexp = "every month, ([0-9]+|last) day.*"
    groups = re.match(regexp, text)

    if groups is not None:
        date_day_number = int(date.strftime("%d"))

        if groups[1] == "last":
            task_day_number = utils.get_month_last_day_date(date).day
        else:
            task_day_number = int(groups[1])

        result = date_day_number == task_day_number and match_pattern_start_date(
            text, date
        )

    return result


def pattern_every_year(text: str, date: datetime.date) -> bool:

    result = False

    day_regexp = get_regexp_for_day_number()
    month_regexp = get_regexp_for_month_name()

    regexp_1 = f".*every year, (?P<d>{day_regexp}) (?P<m>{month_regexp}).*"
    regexp_2 = f".*every year, (?P<m>{month_regexp}) (?P<d>{day_regexp}).*"

    groups = re.match(regexp_1, text)

    if groups is None:
        groups = re.match(regexp_2, text)

    if groups is not None:

        if match_pattern_start_date(text, date):

            months = {
                "jan": 1,
                "feb": 2,
                "mar": 3,
                "apr": 4,
                "may": 5,
                "jun": 6,
                "jul": 7,
                "aug": 8,
                "sep": 9,
                "oct": 10,
                "nov": 11,
                "dec": 12,
            }

            day_number = int(groups["d"])
            month_number = months.get(groups["m"])

            match_pattern_start_date(text, date)

            result = date.day == day_number and date.month == month_number

    return result


def match_pattern_title_and_day_name_for_date(
    text: str, date: datetime.date, regexp: str, day: str
) -> bool:
    result = False

    if match_pattern_title(text, regexp) and date.strftime("%a") == day:
        result = match_pattern_start_date(text, date)

    return result


def match_pattern_start_date(text: str, date: datetime.date) -> bool:

    result = True

    start_date = get_start_date(text)

    if start_date is not None:
        result = date >= start_date

    return result


def match_pattern_title(title: str, regexp: str) -> bool:
    """
    Checks if a title starts with one of the sample strings.
    """

    return re.match(regexp, title, flags=re.IGNORECASE) is not None


def get_start_date(text: str) -> datetime.date:

    date_regexp = get_regexp_for_date()
    full_regexp = f".* from ({date_regexp}).*"

    groups = re.match(full_regexp, text)
    result = None

    if groups is not None:
        result = utils.get_date_from_string(groups[1])

    return result


def get_regexp_for_date() -> str:
    """
    Returns regular expression for a standard date (YYYY-MM-DD).
    """
    return "[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}"


def get_regexp_for_month_name() -> str:
    return "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"


def get_regexp_for_day_number() -> str:
    return "[0-9]{1,2}"


match(Plan("* blabla; every day"), datetime.date.today())
