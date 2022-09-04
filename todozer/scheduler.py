import datetime
import re

from todozer import utils


def match(text: str, date: datetime.date) -> bool:
    """
    каждый второй четверг?..
    """

    matched = False

    text = get_pattern(text)

    if text is None:
        return False

    text = simplify(text)

    patterns = [
        pattern_exact_date,
        pattern_every_day,
        pattern_every_n_day,
        pattern_every_monday,
        pattern_every_tuesday,
        pattern_every_wednesday,
        pattern_every_thursday,
        pattern_every_friday,
        pattern_every_saturday,
        pattern_every_sunday,
        pattern_every_month,
        pattern_every_weekday,
        pattern_every_year,
    ]

    for pattern in patterns:
        matched = pattern(text, date)
        if matched:
            break

    return matched


def get_pattern(text: str) -> str | None:

    index = text.find(';')

    return text[index + 1:].strip() if index != -1 else None


def simplify(text: str) -> str:

    rules = [
        (" с ", " from "),
        ("по будням|по будним дням", "every weekday"),
        ("будний день", "weekday"),
        ("день", "day"),
        ("месяц", "month"),
        ("год", "year"),
        ("дня|дней", "days"),
        ("последний", "last"),
        ("каждый|каждая|каждое", "every"),
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
        ("понедельник|пн|monday", "mon"),
        ("вторник|вт|tuesday", "tue"),
        ("среда|ср|wednesday", "wed"),
        ("четверг|чт|thursday", "thu"),
        ("пятница|пт|friday", "fri"),
        ("суббота|сб|saturday", "sat"),
        ("воскресенье|вс|sunday", "sun"),
    ]

    for rule in rules:

        source_regexp = rf"(.*)({rule[0]})(.*)"
        result_regexp = rf"\1{rule[1]}\3"

        text = re.sub(source_regexp, result_regexp, text, flags=re.IGNORECASE)

    return text


def pattern_exact_date(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - 1983-12-29
    """

    date_regexp = get_regexp_for_date()
    full_regexp = f".*({date_regexp}).*"

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

    if match_pattern_title(text, ["every day"]):
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

    regexp = ".*;.*every ([0-9]+) (day|days).*"
    groups = re.match(regexp, text)

    if groups is not None:

        day_number = int(groups[2])
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

    return match_pattern_title_and_day_name_for_date(text, date, ["every mon"], "Mon")


def pattern_every_tuesday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждый вторник
    - каждый вт
    - every tuesday
    - every tue
    """

    return match_pattern_title_and_day_name_for_date(text, date, ["every tue"], "Tue")


def pattern_every_wednesday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждую среду
    - каждую ср
    - every wednesday
    - every wed
    """

    return match_pattern_title_and_day_name_for_date(text, date, ["every wed"], "Wed")


def pattern_every_thursday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждый четверг
    - каждый чт
    - every thursday
    - every thu
    """

    return match_pattern_title_and_day_name_for_date(text, date, ["every tue"], "Thu")


def pattern_every_friday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждую пятницу
    - каждую пт
    - every friday
    - every fri
    """

    return match_pattern_title_and_day_name_for_date(text, date, ["every fri"], "Fri")


def pattern_every_saturday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждую субботу
    - каждую сб
    - every sat
    """

    return match_pattern_title_and_day_name_for_date(text, date, ["every sat"], "Sat")


def pattern_every_sunday(text: str, date: datetime.date) -> bool:
    """
    Samples:
    - каждое воскресенье
    - каждое вс
    - every sun
    """

    return match_pattern_title_and_day_name_for_date(text, date, ["every sun"], "Sun")


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

    regexp = ".*;.*(weekdays|every weekday).*"
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
    regexp = ".*;.*every month, ([0-9]+|last) day.*"
    groups = re.match(regexp, text)

    if groups is not None:
        date_day_number = int(date.strftime("%d"))

        if groups[2] == "last":
            next_month = date.replace(day=28) + datetime.timedelta(days=4)
            task_day_number = (next_month - datetime.timedelta(days=next_month.day)).day
        else:
            task_day_number = int(groups[2])

        result = date_day_number == task_day_number

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
    text: str, date: datetime.date, samples: list, day: str
) -> bool:
    result = False

    if match_pattern_title(text, samples) and date.strftime("%a") == day:
        result = match_pattern_start_date(text, date)

    return result


def match_pattern_start_date(text: str, date: datetime.date) -> bool:

    result = True

    start_date = get_start_date(text)

    if start_date is not None:
        result = date >= start_date

    return result


def match_pattern_title(title: str, samples: list) -> bool:
    """
    Checks if a title starts with one of the sample strings.
    """

    result = False

    title = title.lower()

    for sample in samples:
        if title.startswith(sample.lower()):
            result = True
            break

    return result


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
