import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def run_test(pattern: str, plan_function):
    yesterday = todozer.utils.get_date_of_yesterday()
    tomorrow = todozer.utils.get_date_of_tomorrow()
    today = todozer.utils.get_date_of_today()

    # If there is no start date at all:

    plan = plan_function(pattern)
    debug_code = tests.helpers.get_debug_code(plan.title_line, today)
    matched_pattern, is_date_matched = match(plan, today)

    assert matched_pattern is Pattern.EVERY_DAY and is_date_matched, debug_code

    # If start date is yesterday:

    plan = plan_function(pattern, yesterday)
    debug_code = tests.helpers.get_debug_code(plan.title_line, today)
    matched_pattern, is_date_matched = match(plan, today)

    assert matched_pattern is Pattern.EVERY_DAY and is_date_matched, debug_code

    # If start date is today:

    plan = plan_function(pattern, today)
    debug_code = tests.helpers.get_debug_code(plan.title_line, today)
    matched_pattern, is_date_matched = match(plan, today)

    assert matched_pattern is Pattern.EVERY_DAY and is_date_matched, debug_code

    # If start date is tomorrow:

    plan = plan_function(pattern, tomorrow)
    debug_code = tests.helpers.get_debug_code(plan.title_line, today)
    matched_pattern, is_date_matched = match(plan, today)

    assert matched_pattern is Pattern.EVERY_DAY and not is_date_matched, debug_code


def test_every_day():
    run_test("каждый день", tests.helpers.get_plan_ru)
    run_test("every day", tests.helpers.get_plan_en)
