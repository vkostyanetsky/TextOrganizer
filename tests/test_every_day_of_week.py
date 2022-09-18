import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match
import datetime


def run_single_test(
    plan_getter,
    plan_pattern: str,
    plan_date: datetime.date | None,
    test_date: datetime.date,
    matched_pattern_value: Pattern,
    is_date_matched_value: bool,
):
    plan = plan_getter(plan_pattern, plan_date)
    debug_code = tests.helpers.get_debug_code(plan.first_line, test_date)
    matched_pattern, is_date_matched = match(plan, test_date)

    assert (
        matched_pattern is matched_pattern_value
        and is_date_matched is is_date_matched_value
    ), debug_code


def run_test_every_day_of_week(
    day_index: int, plan_pattern: str, plan_getter, matched_pattern_value: Pattern
):

    date_of_day = todozer.utils.get_next_day_of_week(day_index)
    date_of_day_plus_1_week = date_of_day + datetime.timedelta(days=7)

    run_single_test(
        plan_getter=plan_getter,
        plan_pattern=plan_pattern,
        plan_date=None,
        test_date=date_of_day,
        matched_pattern_value=matched_pattern_value,
        is_date_matched_value=True,
    )

    run_single_test(
        plan_getter=plan_getter,
        plan_pattern=plan_pattern,
        plan_date=date_of_day,
        test_date=date_of_day,
        matched_pattern_value=matched_pattern_value,
        is_date_matched_value=True,
    )

    run_single_test(
        plan_getter=plan_getter,
        plan_pattern=plan_pattern,
        plan_date=None,
        test_date=date_of_day_plus_1_week,
        matched_pattern_value=matched_pattern_value,
        is_date_matched_value=True,
    )

    run_single_test(
        plan_getter=plan_getter,
        plan_pattern=plan_pattern,
        plan_date=date_of_day_plus_1_week,
        test_date=date_of_day_plus_1_week,
        matched_pattern_value=matched_pattern_value,
        is_date_matched_value=True,
    )


def run_test_every_2_day_of_week(
    day_index: int, plan_pattern: str, plan_getter, matched_pattern_value: Pattern
):

    date_of_day = todozer.utils.get_next_day_of_week(day_index)
    date_of_day_plus_1_week = date_of_day + datetime.timedelta(days=7)
    date_of_day_plus_2_weeks = date_of_day + datetime.timedelta(days=14)

    run_single_test(
        plan_getter=plan_getter,
        plan_pattern=plan_pattern,
        plan_date=date_of_day,
        test_date=date_of_day,
        matched_pattern_value=matched_pattern_value,
        is_date_matched_value=True,
    )

    run_single_test(
        plan_getter=plan_getter,
        plan_pattern=plan_pattern,
        plan_date=date_of_day,
        test_date=date_of_day_plus_1_week,
        matched_pattern_value=matched_pattern_value,
        is_date_matched_value=False,
    )

    run_single_test(
        plan_getter=plan_getter,
        plan_pattern=plan_pattern,
        plan_date=date_of_day,
        test_date=date_of_day_plus_2_weeks,
        matched_pattern_value=matched_pattern_value,
        is_date_matched_value=True,
    )


def test_every_monday():

    day_index = 0
    pattern = Pattern.EVERY_MONDAY
    ru_plan_getter, en_plan_getter = get_plan_getters()

    # ru

    run_test_every_day_of_week(day_index, "каждый понедельник", ru_plan_getter, pattern)
    run_test_every_2_day_of_week(
        day_index, "каждый 2 понедельник", ru_plan_getter, pattern
    )

    # en

    run_test_every_day_of_week(day_index, "every monday", en_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "every 2 monday", en_plan_getter, pattern)


def test_every_tuesday():

    day_index = 1
    pattern = Pattern.EVERY_TUESDAY
    ru_plan_getter, en_plan_getter = get_plan_getters()

    # ru

    run_test_every_day_of_week(day_index, "каждый вторник", ru_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "каждый 2 вторник", ru_plan_getter, pattern)

    # en

    run_test_every_day_of_week(day_index, "every tuesday", en_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "every 2 tuesday", en_plan_getter, pattern)


def test_every_wednesday():

    day_index = 2
    pattern = Pattern.EVERY_WEDNESDAY
    ru_plan_getter, en_plan_getter = get_plan_getters()

    run_test_every_day_of_week(day_index, "каждую среду", ru_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "каждую 2 среду", ru_plan_getter, pattern)

    run_test_every_day_of_week(day_index, "every wednesday", en_plan_getter, pattern)
    run_test_every_2_day_of_week(
        day_index, "every 2 wednesday", en_plan_getter, pattern
    )


def test_every_thursday():

    day_index = 3
    pattern = Pattern.EVERY_THURSDAY
    ru_plan_getter, en_plan_getter = get_plan_getters()

    run_test_every_day_of_week(day_index, "каждый четверг", ru_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "каждый 2 четверг", ru_plan_getter, pattern)

    run_test_every_day_of_week(day_index, "every thursday", en_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "every 2 thursday", en_plan_getter, pattern)


def test_every_friday():

    day_index = 4
    pattern = Pattern.EVERY_FRIDAY
    ru_plan_getter, en_plan_getter = get_plan_getters()

    run_test_every_day_of_week(day_index, "каждую пятницу", ru_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "каждую 2 пятницу", ru_plan_getter, pattern)

    run_test_every_day_of_week(day_index, "every friday", en_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "every 2 friday", en_plan_getter, pattern)


def test_every_saturday():

    day_index = 5
    pattern = Pattern.EVERY_SATURDAY
    ru_plan_getter, en_plan_getter = get_plan_getters()

    run_test_every_day_of_week(day_index, "каждую субботу", ru_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "каждую 2 субботу", ru_plan_getter, pattern)

    run_test_every_day_of_week(day_index, "every saturday", en_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "every 2 saturday", en_plan_getter, pattern)


def test_every_sunday():

    day_index = 6
    pattern = Pattern.EVERY_SUNDAY
    ru_plan_getter, en_plan_getter = get_plan_getters()

    run_test_every_day_of_week(day_index, "каждое воскресенье", ru_plan_getter, pattern)
    run_test_every_2_day_of_week(
        day_index, "каждое 2 воскресенье", ru_plan_getter, pattern
    )

    run_test_every_day_of_week(day_index, "every sunday", en_plan_getter, pattern)
    run_test_every_2_day_of_week(day_index, "every 2 sunday", en_plan_getter, pattern)


def get_plan_getters():

    return tests.helpers.get_plan_en, tests.helpers.get_plan_ru
