import datetime

import tests
from todozer import scheduler


def get_date(day: int) -> datetime.date:
    from_date = datetime.date.today()
    day_index = from_date.weekday()

    different_days = day - day_index if day_index < day else 7 - day_index + day

    return from_date + datetime.timedelta(days=different_days)


def run_test(day_index: int, pattern: str, task_text_function):

    date_of_day = get_date(day_index)
    date_of_day_after = tests.get_tomorrow_date(date_of_day)
    date_of_day_before = tests.get_yesterday_date(date_of_day)

    # If day of week is today:

    task_text = task_text_function(pattern)
    assert scheduler.match(task_text, date_of_day) is True

    task_text = task_text_function(pattern, date_of_day_before)
    assert scheduler.match(task_text, date_of_day) is True

    task_text = task_text_function(pattern, date_of_day)
    assert scheduler.match(task_text, date_of_day) is True

    task_text = task_text_function(pattern, date_of_day_after)
    assert scheduler.match(task_text, date_of_day) is False

    # If day of week is yesterday:

    task_text = task_text_function(pattern)
    assert scheduler.match(task_text, date_of_day_before) is False

    task_text = task_text_function(pattern, date_of_day_before)
    assert scheduler.match(task_text, date_of_day_before) is False

    task_text = task_text_function(pattern, date_of_day)
    assert scheduler.match(task_text, date_of_day_before) is False

    task_text = task_text_function(pattern, date_of_day_after)
    assert scheduler.match(task_text, date_of_day_before) is False

    # If day of week is tomorrow:

    task_text = task_text_function(pattern)
    assert scheduler.match(task_text, date_of_day_after) is False

    task_text = task_text_function(pattern, date_of_day_before)
    assert scheduler.match(task_text, date_of_day_after) is False

    task_text = task_text_function(pattern, date_of_day)
    assert scheduler.match(task_text, date_of_day_after) is False

    task_text = task_text_function(pattern, date_of_day_after)
    assert scheduler.match(task_text, date_of_day_after) is False


def test_every_monday():

    day_index = 0

    # ru

    run_test(day_index, "каждый понедельник", tests.get_task_text_ru)
    run_test(day_index, "каждый Пн", tests.get_task_text_ru)

    # en

    run_test(day_index, "every monday", tests.get_task_text_en)
    run_test(day_index, "every Mon", tests.get_task_text_en)


def test_every_tuesday():

    day_index = 1

    # ru

    run_test(day_index, "каждый вторник", tests.get_task_text_ru)
    run_test(day_index, "каждый Вт", tests.get_task_text_ru)

    # en

    run_test(day_index, "every tuesday", tests.get_task_text_en)
    run_test(day_index, "every Tue", tests.get_task_text_en)


def test_every_wednesday():

    day_index = 2

    # ru

    run_test(day_index, "каждую среду", tests.get_task_text_ru)
    run_test(day_index, "каждую Ср", tests.get_task_text_ru)

    # en

    run_test(day_index, "every wednesday", tests.get_task_text_en)
    run_test(day_index, "every Wed", tests.get_task_text_en)


def test_every_thursday():

    day_index = 3

    # ru

    run_test(day_index, "каждый четверг", tests.get_task_text_ru)
    run_test(day_index, "каждый Чт", tests.get_task_text_ru)

    # en

    run_test(day_index, "every thursday", tests.get_task_text_en)
    run_test(day_index, "every Thu", tests.get_task_text_en)


def test_every_friday():

    day_index = 4

    # ru

    run_test(day_index, "каждую пятницу", tests.get_task_text_ru)
    run_test(day_index, "каждую Пт", tests.get_task_text_ru)

    # en

    run_test(day_index, "every friday", tests.get_task_text_en)
    run_test(day_index, "every Fri", tests.get_task_text_en)


def test_every_saturday():

    day_index = 5

    # ru

    run_test(day_index, "каждую субботу", tests.get_task_text_ru)
    run_test(day_index, "каждую Сб", tests.get_task_text_ru)

    # en

    run_test(day_index, "every saturday", tests.get_task_text_en)
    run_test(day_index, "every Sat", tests.get_task_text_en)


def test_every_sunday():

    day_index = 6

    # ru

    run_test(day_index, "каждое воскресенье", tests.get_task_text_ru)
    run_test(day_index, "каждое Вс", tests.get_task_text_ru)

    # en

    run_test(day_index, "every sunday", tests.get_task_text_en)
    run_test(day_index, "every Sun", tests.get_task_text_en)
