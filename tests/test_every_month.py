import datetime

import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def plan_ru(day: str | int, start_date: datetime.date | None = None):
    return tests.helpers.get_plan_ru(f"каждый месяц, {day} день", start_date)


def plan_en(day: str | int, start_date: datetime.date | None = None):
    return tests.helpers.get_plan_en(f"every month, {day} day", start_date)


def run_test(date: datetime.date, plan_function):

    yesterday = date - datetime.timedelta(days=1)
    tomorrow = date + datetime.timedelta(days=1)

    # The task date is today, but we try to match it yesterday:

    plan = plan_function(date.day)
    assert match(plan, yesterday) is not Pattern.EVERY_MONTH

    # The task date is today:

    plan = plan_function(date.day)
    assert match(plan, date) is Pattern.EVERY_MONTH

    # The task date is today, and it starts yesterday:

    plan = plan_function(date.day, yesterday)
    assert match(plan, date) is Pattern.EVERY_MONTH

    # The task date is today, and it starts today:

    plan = plan_function(date.day, date)
    assert match(plan, date) is Pattern.EVERY_MONTH

    # The task date is today, and it starts tomorrow:

    plan = plan_function(date.day, tomorrow)
    assert match(plan, date) is not Pattern.EVERY_MONTH


def test_every_month():

    this_day = todozer.utils.get_date_of_today()
    last_day = todozer.utils.get_month_last_day_date(this_day)

    # ru

    run_test(this_day, plan_ru)
    run_test(last_day, plan_ru)

    # en

    run_test(this_day, plan_en)
    run_test(last_day, plan_en)
