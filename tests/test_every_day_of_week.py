import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def run_test(day_index: int, pattern: str, plan_function, assert_to: Pattern):

    date_of_day = tests.helpers.get_day_of_week(day_index)
    date_of_day_after = todozer.utils.get_date_of_tomorrow(date_of_day)
    date_of_day_before = todozer.utils.get_date_of_yesterday(date_of_day)

    # If day of week is today:

    plan = plan_function(pattern)
    matched_pattern, is_date_matched = match(plan, date_of_day)
    assert matched_pattern is assert_to and is_date_matched

    plan = plan_function(pattern, date_of_day_before)
    matched_pattern, is_date_matched = match(plan, date_of_day)
    assert matched_pattern is assert_to and is_date_matched

    plan = plan_function(pattern, date_of_day)
    matched_pattern, is_date_matched = match(plan, date_of_day)
    assert matched_pattern is assert_to and is_date_matched

    plan = plan_function(pattern, date_of_day_after)
    matched_pattern, is_date_matched = match(plan, date_of_day)
    assert matched_pattern is assert_to and not is_date_matched

    # If day of week is yesterday:

    plan = plan_function(pattern)
    matched_pattern, is_date_matched = match(plan, date_of_day_before)
    assert matched_pattern is assert_to and not is_date_matched

    plan = plan_function(pattern, date_of_day_before)
    matched_pattern, is_date_matched = match(plan, date_of_day_before)
    assert matched_pattern is assert_to and not is_date_matched

    plan = plan_function(pattern, date_of_day)
    matched_pattern, is_date_matched = match(plan, date_of_day_before)
    assert matched_pattern is assert_to and not is_date_matched

    plan = plan_function(pattern, date_of_day_after)
    matched_pattern, is_date_matched = match(plan, date_of_day_before)
    assert matched_pattern is assert_to and not is_date_matched

    # If day of week is tomorrow:

    plan = plan_function(pattern)
    matched_pattern, is_date_matched = match(plan, date_of_day_after)
    assert matched_pattern is assert_to and not is_date_matched

    plan = plan_function(pattern, date_of_day_before)
    matched_pattern, is_date_matched = match(plan, date_of_day_after)
    assert matched_pattern is assert_to and not is_date_matched

    plan = plan_function(pattern, date_of_day)
    matched_pattern, is_date_matched = match(plan, date_of_day_after)
    assert matched_pattern is assert_to and not is_date_matched

    plan = plan_function(pattern, date_of_day_after)
    matched_pattern, is_date_matched = match(plan, date_of_day_after)
    assert matched_pattern is assert_to and not is_date_matched


def test_every_monday():

    day_index = 0

    # ru

    run_test(
        day_index, "каждый понедельник", tests.helpers.get_plan_ru, Pattern.EVERY_MONDAY
    )

    # en

    run_test(day_index, "every monday", tests.helpers.get_plan_en, Pattern.EVERY_MONDAY)


def test_every_tuesday():

    day_index = 1

    # ru

    run_test(
        day_index, "каждый вторник", tests.helpers.get_plan_ru, Pattern.EVERY_TUESDAY
    )

    # en

    run_test(
        day_index, "every tuesday", tests.helpers.get_plan_en, Pattern.EVERY_TUESDAY
    )


def test_every_wednesday():

    day_index = 2

    # ru

    run_test(
        day_index, "каждую среду", tests.helpers.get_plan_ru, Pattern.EVERY_WEDNESDAY
    )

    # en

    run_test(
        day_index, "every wednesday", tests.helpers.get_plan_en, Pattern.EVERY_WEDNESDAY
    )


def test_every_thursday():

    day_index = 3

    # ru

    run_test(
        day_index, "каждый четверг", tests.helpers.get_plan_ru, Pattern.EVERY_THURSDAY
    )

    # en

    run_test(
        day_index, "every thursday", tests.helpers.get_plan_en, Pattern.EVERY_THURSDAY
    )


def test_every_friday():

    day_index = 4

    # ru

    run_test(
        day_index, "каждую пятницу", tests.helpers.get_plan_ru, Pattern.EVERY_FRIDAY
    )

    # en

    run_test(day_index, "every friday", tests.helpers.get_plan_en, Pattern.EVERY_FRIDAY)


def test_every_saturday():

    day_index = 5

    # ru

    run_test(
        day_index, "каждую субботу", tests.helpers.get_plan_ru, Pattern.EVERY_SATURDAY
    )

    # en

    run_test(
        day_index, "every saturday", tests.helpers.get_plan_en, Pattern.EVERY_SATURDAY
    )


def test_every_sunday():

    day_index = 6

    # ru

    run_test(
        day_index, "каждое воскресенье", tests.helpers.get_plan_ru, Pattern.EVERY_SUNDAY
    )

    # en

    run_test(day_index, "every sunday", tests.helpers.get_plan_en, Pattern.EVERY_SUNDAY)
