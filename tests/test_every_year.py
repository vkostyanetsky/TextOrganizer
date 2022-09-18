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

    debug_code = tests.helpers.get_debug_code(plan.first_line, today)
    matched_pattern, is_date_matched = match(plan, today)

    return matched_pattern is Pattern.EVERY_YEAR and is_date_matched, debug_code


def match_en(task_date: datetime.date, start_date: datetime.date = None):

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    plan_date = task_date.strftime("%B %d")
    plan = tests.helpers.get_plan_en(f"every year, {plan_date}", start_date)

    today = todozer.utils.get_date_of_today()

    debug_code = tests.helpers.get_debug_code(plan.first_line, today)
    matched_pattern, is_date_matched = match(plan, today)

    return matched_pattern is Pattern.EVERY_YEAR and is_date_matched, debug_code


def test_every_year():

    yesterday = todozer.utils.get_date_of_yesterday()
    tomorrow = todozer.utils.get_date_of_tomorrow()
    today = todozer.utils.get_date_of_today()

    # ru

    result, debug_code = match_ru(task_date=today)
    assert result is True, debug_code

    result, debug_code = match_ru(task_date=today, start_date=yesterday)
    assert result is True, debug_code

    result, debug_code = match_ru(task_date=today, start_date=tomorrow)
    assert result is False, debug_code

    result, debug_code = match_ru(task_date=tomorrow)
    assert result is False, debug_code

    result, debug_code = match_ru(task_date=tomorrow, start_date=yesterday)
    assert result is False, debug_code

    result, debug_code = match_ru(task_date=tomorrow, start_date=tomorrow)
    assert result is False, debug_code

    # en

    result, debug_code = match_en(task_date=today)
    assert result is True, debug_code

    result, debug_code = match_en(task_date=today, start_date=yesterday)
    assert result is True, debug_code

    result, debug_code = match_en(task_date=today, start_date=tomorrow)
    assert result is False, debug_code

    result, debug_code = match_en(task_date=tomorrow)
    assert result is False, debug_code

    result, debug_code = match_en(task_date=tomorrow, start_date=yesterday)
    assert result is False, debug_code

    result, debug_code = match_en(task_date=tomorrow, start_date=tomorrow)
    assert result is False, debug_code
