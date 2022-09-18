import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def test_every_month():

    run_test(
        [
            "по будням",
            "по будним дням",
            "каждый будний день",
        ],
        tests.helpers.get_plan_ru,
    )

    run_test(
        [
            "weekdays",
            "every weekday",
        ],
        tests.helpers.get_plan_en,
    )


def run_test(variants: list, plan_function):

    monday = tests.helpers.get_day_of_week(0)
    before_monday = todozer.utils.get_date_of_yesterday(monday)
    after_monday = todozer.utils.get_date_of_tomorrow(monday)

    sunday = tests.helpers.get_day_of_week(6)
    before_sunday = todozer.utils.get_date_of_yesterday(sunday)
    after_sunday = todozer.utils.get_date_of_tomorrow(sunday)

    for variant in variants:

        plan = plan_function(variant)
        debug_code = tests.helpers.get_debug_code(plan.first_line, monday)
        matched_pattern, is_date_matched = match(plan, monday)
        assert matched_pattern is Pattern.EVERY_WEEKDAY and is_date_matched, debug_code

        plan = plan_function(variant, before_monday)
        debug_code = tests.helpers.get_debug_code(plan.first_line, monday)
        matched_pattern, is_date_matched = match(plan, monday)
        assert matched_pattern is Pattern.EVERY_WEEKDAY and is_date_matched, debug_code

        plan = plan_function(variant, monday)
        debug_code = tests.helpers.get_debug_code(plan.first_line, monday)
        matched_pattern, is_date_matched = match(plan, monday)
        assert matched_pattern is Pattern.EVERY_WEEKDAY and is_date_matched, debug_code

        plan = plan_function(variant, after_monday)
        debug_code = tests.helpers.get_debug_code(plan.first_line, monday)
        matched_pattern, is_date_matched = match(plan, monday)
        assert (
            matched_pattern is Pattern.EVERY_WEEKDAY and not is_date_matched
        ), debug_code

        plan = plan_function(variant)
        debug_code = tests.helpers.get_debug_code(plan.first_line, sunday)
        matched_pattern, is_date_matched = match(plan, sunday)
        assert (
            matched_pattern is Pattern.EVERY_WEEKDAY and not is_date_matched
        ), debug_code

        plan = plan_function(variant, before_sunday)
        debug_code = tests.helpers.get_debug_code(plan.first_line, sunday)
        matched_pattern, is_date_matched = match(plan, sunday)
        assert (
            matched_pattern is Pattern.EVERY_WEEKDAY and not is_date_matched
        ), debug_code

        plan = plan_function(variant, sunday)
        debug_code = tests.helpers.get_debug_code(plan.first_line, sunday)
        matched_pattern, is_date_matched = match(plan, sunday)
        assert (
            matched_pattern is Pattern.EVERY_WEEKDAY and not is_date_matched
        ), debug_code

        plan = plan_function(variant, after_sunday)
        debug_code = tests.helpers.get_debug_code(plan.first_line, sunday)
        matched_pattern, is_date_matched = match(plan, sunday)
        assert (
            matched_pattern is Pattern.EVERY_WEEKDAY and not is_date_matched
        ), debug_code
