import datetime
import locale

import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def match_ru(task_date: datetime.date, start_date: datetime.date = None):

    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

    plan_date = task_date.strftime("%d %B")
    plan = tests.helpers.get_plan_ru(f"каждый год, {plan_date}", start_date)

    today = todozer.utils.get_date_of_today()

    return match(plan, today) is Pattern.EVERY_YEAR


def match_en(task_date: datetime.date, start_date: datetime.date = None):

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    plan_date = task_date.strftime("%B %d")
    plan = tests.helpers.get_plan_en(f"every year, {plan_date}", start_date)

    today = todozer.utils.get_date_of_today()

    return match(plan, today) is Pattern.EVERY_YEAR


def test_every_year():

    yesterday = todozer.utils.get_date_of_yesterday()
    tomorrow = todozer.utils.get_date_of_tomorrow()
    today = todozer.utils.get_date_of_today()

    # ru

    assert match_ru(task_date=today) is True
    assert match_ru(task_date=today, start_date=yesterday) is True
    assert match_ru(task_date=today, start_date=tomorrow) is False

    assert match_ru(task_date=tomorrow) is False
    assert match_ru(task_date=tomorrow, start_date=yesterday) is False
    assert match_ru(task_date=tomorrow, start_date=tomorrow) is False

    # en

    assert match_en(task_date=today) is True
    assert match_en(task_date=today, start_date=yesterday) is True
    assert match_en(task_date=today, start_date=tomorrow) is False

    assert match_en(task_date=tomorrow) is False
    assert match_en(task_date=tomorrow, start_date=yesterday) is False
    assert match_en(task_date=tomorrow, start_date=tomorrow) is False
