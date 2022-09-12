import tests.helpers
import todozer.scheduler
import todozer.utils


def run_test(day_index: int, pattern: str, plan_function):

    date_of_day = tests.helpers.get_day_of_week(day_index)
    date_of_day_after = todozer.utils.get_date_of_tomorrow(date_of_day)
    date_of_day_before = todozer.utils.get_date_of_yesterday(date_of_day)

    # If day of week is today:

    plan = plan_function(pattern)
    assert todozer.scheduler.match(plan, date_of_day) is True

    plan = plan_function(pattern, date_of_day_before)
    assert todozer.scheduler.match(plan, date_of_day) is True

    plan = plan_function(pattern, date_of_day)
    assert todozer.scheduler.match(plan, date_of_day) is True

    plan = plan_function(pattern, date_of_day_after)
    assert todozer.scheduler.match(plan, date_of_day) is False

    # If day of week is yesterday:

    plan = plan_function(pattern)
    assert todozer.scheduler.match(plan, date_of_day_before) is False

    plan = plan_function(pattern, date_of_day_before)
    assert todozer.scheduler.match(plan, date_of_day_before) is False

    plan = plan_function(pattern, date_of_day)
    assert todozer.scheduler.match(plan, date_of_day_before) is False

    plan = plan_function(pattern, date_of_day_after)
    assert todozer.scheduler.match(plan, date_of_day_before) is False

    # If day of week is tomorrow:

    plan = plan_function(pattern)
    assert todozer.scheduler.match(plan, date_of_day_after) is False

    plan = plan_function(pattern, date_of_day_before)
    assert todozer.scheduler.match(plan, date_of_day_after) is False

    plan = plan_function(pattern, date_of_day)
    assert todozer.scheduler.match(plan, date_of_day_after) is False

    plan = plan_function(pattern, date_of_day_after)
    assert todozer.scheduler.match(plan, date_of_day_after) is False


def test_every_monday():

    day_index = 0

    # ru

    run_test(day_index, "каждый понедельник", tests.helpers.get_plan_ru)
    # run_test(day_index, "каждый Пн", tests.helpers.get_plan_ru)

    # en

    run_test(day_index, "every monday", tests.helpers.get_plan_en)
    # run_test(day_index, "every Mon", tests.helpers.get_plan_en)


def test_every_tuesday():

    day_index = 1

    # ru

    run_test(day_index, "каждый вторник", tests.helpers.get_plan_ru)
    # run_test(day_index, "каждый Вт", tests.helpers.get_plan_ru)

    # en

    run_test(day_index, "every tuesday", tests.helpers.get_plan_en)
    # run_test(day_index, "every Tue", tests.helpers.get_plan_en)


def test_every_wednesday():

    day_index = 2

    # ru

    run_test(day_index, "каждую среду", tests.helpers.get_plan_ru)
    # run_test(day_index, "каждую Ср", tests.helpers.get_plan_ru)

    # en

    run_test(day_index, "every wednesday", tests.helpers.get_plan_en)
    # run_test(day_index, "every Wed", tests.helpers.get_plan_en)


def test_every_thursday():

    day_index = 3

    # ru

    run_test(day_index, "каждый четверг", tests.helpers.get_plan_ru)
    # run_test(day_index, "каждый Чт", tests.helpers.get_plan_ru)

    # en

    run_test(day_index, "every thursday", tests.helpers.get_plan_en)
    # run_test(day_index, "every Thu", tests.helpers.get_plan_en)


def test_every_friday():

    day_index = 4

    # ru

    run_test(day_index, "каждую пятницу", tests.helpers.get_plan_ru)
    # run_test(day_index, "каждую Пт", tests.helpers.get_plan_ru)

    # en

    run_test(day_index, "every friday", tests.helpers.get_plan_en)
    # run_test(day_index, "every Fri", tests.helpers.get_plan_en)


def test_every_saturday():

    day_index = 5

    # ru

    run_test(day_index, "каждую субботу", tests.helpers.get_plan_ru)
    # run_test(day_index, "каждую Сб", tests.helpers.get_plan_ru)

    # en

    run_test(day_index, "every saturday", tests.helpers.get_plan_en)
    # run_test(day_index, "every Sat", tests.helpers.get_plan_en)


def test_every_sunday():

    day_index = 6

    # ru

    run_test(day_index, "каждое воскресенье", tests.helpers.get_plan_ru)
    # run_test(day_index, "каждое Вс", tests.helpers.get_plan_ru)

    # en

    run_test(day_index, "every sunday", tests.helpers.get_plan_en)
    # run_test(day_index, "every Sun", tests.helpers.get_plan_en)
