import tests.helpers as helpers
import todozer.scheduler


def run_test_every_day(pattern: str, task_text_function):

    # No start date:

    task_text = task_text_function(pattern)

    assert todozer.scheduler.match(task_text, helpers.get_today_date()) is True

    # If start date is yesterday:

    task_date = helpers.get_yesterday_date()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, helpers.get_today_date()) is True

    # If start date is today:

    task_date = helpers.get_today_date()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, helpers.get_today_date()) is True

    # If start date is tomorrow:

    task_date = helpers.get_tomorrow_date()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, helpers.get_today_date()) is False


def test_every_day():

    run_test_every_day("каждый день", helpers.get_task_text_ru)
    run_test_every_day("every day", helpers.get_task_text_en)
