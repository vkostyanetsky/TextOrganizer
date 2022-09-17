import datetime
import enum
import logging
import re

from todozer import parser, utils


class Pattern(enum.Enum):
    """Task repetition patterns."""

    NONE = enum.auto()
    EXACT_DATE = enum.auto()
    EVERY_DAY = enum.auto()
    EVERY_N_DAY = enum.auto()
    EVERY_MONTH = enum.auto()
    EVERY_WEEKDAY = enum.auto()
    EVERY_YEAR = enum.auto()
    EVERY_MONDAY = enum.auto()
    EVERY_TUESDAY = enum.auto()
    EVERY_WEDNESDAY = enum.auto()
    EVERY_THURSDAY = enum.auto()
    EVERY_FRIDAY = enum.auto()
    EVERY_SATURDAY = enum.auto()
    EVERY_SUNDAY = enum.auto()


class BasicPattern:
    name: Pattern = Pattern.NONE
    line: str

    def __init__(self, line: str):
        self.line = line

    def parse(self):
        pass

    def match(self):
        pass

    def match_title(self, regexp: str) -> bool:
        """
        Checks if a line equals the provided regexp.
        """

        return re.match(regexp, self.line, flags=re.IGNORECASE) is not None

    def match_start_date(self, date: datetime.date) -> bool:

        result = True

        start_date = self.get_start_date()

        if start_date is not None:
            result = date >= start_date

        return result

    def get_start_date(self) -> datetime.date:

        date_regexp = utils.get_regexp_for_date()
        full_regexp = f".* from ({date_regexp}).*"

        groups = re.match(full_regexp, self.line)
        result = None

        if groups is not None:
            result = utils.get_date_from_string(groups[1])

        return result


class ExactDatePattern(BasicPattern):
    """
    Samples:
    - 1983-12-29
    """

    name: Pattern = Pattern.EXACT_DATE

    def __init__(self, line: str):
        super().__init__(line)

        self.exact_date = None

    def parse(self):
        date_regexp = utils.get_regexp_for_date()
        full_regexp = f"({date_regexp}).*"

        groups = re.match(full_regexp, self.line)

        if groups is not None:
            self.exact_date = utils.get_date_from_string(groups[1])

    def match_line(self) -> bool:
        return self.exact_date is not None

    def match_date(self, date: datetime.date) -> bool:
        return date == self.exact_date


class EveryDayPattern(BasicPattern):
    """
    Samples:
    - каждый день
    - every day
    """

    name: Pattern = Pattern.EVERY_DAY

    def match_line(self) -> bool:
        return self.match_title("every day.*")

    def match_date(self, date: datetime.date) -> bool:
        return self.match_start_date(date)


class EveryNDayPattern(BasicPattern):
    """
    Samples:
    - каждый 1 день
    - каждые 2 дня
    - каждые 5 дней
    - every 1 day
    - every 3 days
    """

    name: Pattern = Pattern.EVERY_N_DAY

    def __init__(self, line: str):
        super().__init__(line)

        self.day_number = None
        self.start_date = None

    def parse(self):
        regexp = ".*every ([0-9]+) day.*"
        groups = re.match(regexp, self.line)

        if groups is not None:
            self.day_number = int(groups[1])
            self.start_date = self.get_start_date()

    def match_line(self) -> bool:
        return self.start_date is not None

    def match_date(self, date: datetime.date) -> bool:
        return (
            date >= self.start_date
            and abs(date - self.start_date).days % self.day_number == 0
        )


class EveryMondayPattern(BasicPattern):
    """
    Samples:
    - каждый понедельник
    - every monday
    """

    name: Pattern = Pattern.EVERY_MONDAY

    def match_line(self) -> bool:
        return self.match_title("every monday")

    def match_date(self, date: datetime.date) -> bool:
        return date.strftime("%a") == "Mon" and self.match_start_date(date)


class EveryTuesdayPattern(BasicPattern):
    """
    Samples:
    - каждый вторник
    - every tuesday
    """

    name: Pattern = Pattern.EVERY_TUESDAY

    def match_line(self) -> bool:
        return self.match_title("every tuesday")

    def match_date(self, date: datetime.date) -> bool:
        return date.strftime("%a") == "Tue" and self.match_start_date(date)


class EveryWednesdayPattern(BasicPattern):
    """
    Samples:
    - каждую среду
    - every wednesday
    """

    name: Pattern = Pattern.EVERY_WEDNESDAY

    def match_line(self) -> bool:
        return self.match_title("every wednesday")

    def match_date(self, date: datetime.date) -> bool:
        return date.strftime("%a") == "Wed" and self.match_start_date(date)


class EveryThursdayPattern(BasicPattern):
    """
    Samples:
    - каждый четверг
    - every thursday
    """

    name: Pattern = Pattern.EVERY_THURSDAY

    def match_line(self) -> bool:
        return self.match_title("every thursday")

    def match_date(self, date: datetime.date) -> bool:
        return date.strftime("%a") == "Thu" and self.match_start_date(date)


class EveryFridayPattern(BasicPattern):
    """
    Samples:
    - каждую пятницу
    - every friday
    """

    name: Pattern = Pattern.EVERY_FRIDAY

    def match_line(self) -> bool:
        return self.match_title("every friday")

    def match_date(self, date: datetime.date) -> bool:
        return date.strftime("%a") == "Fri" and self.match_start_date(date)


class EverySaturdayPattern(BasicPattern):
    """
    Samples:
    - каждую субботу
    - every saturday
    """

    name: Pattern = Pattern.EVERY_SATURDAY

    def match_line(self) -> bool:
        return self.match_title("every saturday")

    def match_date(self, date: datetime.date) -> bool:
        return date.strftime("%a") == "Sat" and self.match_start_date(date)


class EverySundayPattern(BasicPattern):
    """
    Samples:
    - каждое воскресенье
    - every sunday
    """

    name: Pattern = Pattern.EVERY_SUNDAY

    def match_line(self) -> bool:
        return self.match_title("every sunday")

    def match_date(self, date: datetime.date) -> bool:
        return date.strftime("%a") == "Sun" and self.match_start_date(date)


class EveryWeekdayPattern(BasicPattern):
    """
    Samples:
    - по будням
    - по будним дням
    - каждый будний день
    - weekdays
    - every weekday
    """

    name: Pattern = Pattern.EVERY_WEEKDAY

    def match_line(self) -> bool:
        regexp = "(weekdays|every weekday).*"

        return re.match(regexp, self.line) is not None

    def match_date(self, date: datetime.date) -> bool:

        return 0 <= date.weekday() <= 4 and self.match_start_date(date)


class EveryMonthPattern(BasicPattern):
    """
    Samples:
    - каждый месяц, 5 день
    - каждый месяц, последний день
    - каждый месяц, 5 день, начиная с 29.12.1983
    - каждый месяц, 5 день с 29.12.1983
    - every month, day 5
    - every month, 5 day
    - every month, last day
    """

    name: Pattern = Pattern.EVERY_MONTH

    def __init__(self, line: str):
        super().__init__(line)

        self.day = None

    def parse(self):
        regexp_1 = "every month, ([0-9]+|last) day.*"
        regexp_2 = "every month, day ([0-9]+).*"

        groups = re.match(regexp_1, self.line)

        if groups is None:
            groups = re.match(regexp_2, self.line)

        if groups is not None:
            self.day = groups[1]

    def match_line(self) -> bool:
        return self.day is not None

    def match_date(self, date: datetime.date) -> bool:
        date_day_number = int(date.strftime("%d"))

        if self.day == "last":
            task_day_number = utils.get_month_last_day_date(date).day
        else:
            task_day_number = int(self.day)

        return date_day_number == task_day_number and self.match_start_date(date)


class EveryYearPattern(BasicPattern):
    """
    Samples:
    - каждый год, 1 апреля
    - every year, 1 April
    """

    name: Pattern = Pattern.EVERY_YEAR

    def __init__(self, line: str):
        super().__init__(line)

        self.day = None
        self.month = None

    def parse(self):
        day_regexp = "[0-9]{1,2}"
        month_regexp = "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"

        regexp_1 = f".*every year, (?P<d>{day_regexp}) (?P<m>{month_regexp}).*"
        regexp_2 = f".*every year, (?P<m>{month_regexp}) (?P<d>{day_regexp}).*"

        groups = re.match(regexp_1, self.line)

        if groups is None:
            groups = re.match(regexp_2, self.line)

        if groups is not None:
            self.day = groups["d"]
            self.month = groups["m"]

    def match_line(self) -> bool:
        return self.day is not None and self.month is not None

    def match_date(self, date: datetime.date) -> bool:

        result = False

        if self.match_start_date(date):

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

            day_number = int(self.day)
            month_number = months.get(self.month)

            result = date.day == day_number and date.month == month_number

        return result


def match(plan: parser.Plan, date: datetime.date) -> tuple:

    matched_pattern = Pattern.NONE
    is_date_matched = False

    logging.debug(
        f'Attempt to match pattern for "{str(plan)}" on {utils.get_string_from_date(date)}'
    )

    if plan.pattern == "":
        logging.debug("Pattern text is not found.")
    else:
        pattern_text = get_compiled_pattern(plan.pattern)

        logging.debug("Pattern text: %s (compiled: %s)", plan.pattern, pattern_text)

        patterns = {
            ExactDatePattern,
            EveryDayPattern,
            EveryNDayPattern,
            EveryMonthPattern,
            EveryWeekdayPattern,
            EveryYearPattern,
            EveryMondayPattern,
            EveryTuesdayPattern,
            EveryWednesdayPattern,
            EveryThursdayPattern,
            EveryFridayPattern,
            EverySaturdayPattern,
            EverySundayPattern,
        }

        logging.debug("Matching the pattern...")

        for pattern in patterns:

            logging.debug('Checking a pattern: "%s"...', pattern.name)

            pattern_object = pattern(pattern_text)
            pattern_object.parse()

            line_matched = pattern_object.match_line()

            if line_matched:

                logging.debug("Line is matched!")

                matched_pattern = pattern_object.name
                is_date_matched = pattern_object.match_date(date)

                if is_date_matched:
                    logging.debug("Date is matched!")
                else:
                    logging.debug("Date is not matched.")

                break

    return matched_pattern, is_date_matched


def get_compiled_pattern(text: str) -> str:

    rules = [
        (" с ", " from "),
        ("по будням|по будним дням", "every weekday"),
        ("будний день", "weekday"),
        ("день", "day"),
        (" days", " day"),
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

from todozer import parser
t = parser.Plan(" - Bob, do something!; every 3 days from 2022-09-18")
match(t, datetime.datetime.today().date())
