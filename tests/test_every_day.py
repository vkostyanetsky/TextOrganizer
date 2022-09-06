import tests
from todozer import scheduler


def run_test_every_day(pattern: str, task_text_function):

    # No start date:

    task_text = task_text_function(pattern)

    assert scheduler.match(task_text, tests.get_today_date()) is True

    # If start date is yesterday:

    task_date = tests.get_yesterday_date()
    task_text = task_text_function(pattern, task_date)

    assert scheduler.match(task_text, tests.get_today_date()) is True

    # If start date is today:

    task_date = tests.get_today_date()
    task_text = task_text_function(pattern, task_date)

    assert scheduler.match(task_text, tests.get_today_date()) is True

    # If start date is tomorrow:

    task_date = tests.get_tomorrow_date()
    task_text = task_text_function(pattern, task_date)

    assert scheduler.match(task_text, tests.get_today_date()) is False


def test_every_day():

    run_test_every_day("каждый день", tests.get_task_text_ru)
    run_test_every_day("every day", tests.get_task_text_en)
