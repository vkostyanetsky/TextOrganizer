import tests.helpers
import todozer.scheduler


def run_test(pattern: str, task_text_function):

    today = tests.helpers.get_today_date()

    # If there is no start date at all:

    task_text = task_text_function(pattern)

    assert todozer.scheduler.match(task_text, today) is True

    # If start date is yesterday:

    task_date = tests.helpers.get_yesterday_date()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, today) is True

    # If start date is today:

    task_date = tests.helpers.get_today_date()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, today) is True

    # If start date is tomorrow:

    task_date = tests.helpers.get_tomorrow_date()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, today) is False


def test_every_day():

    run_test("каждый день", tests.helpers.get_task_text_ru)
    run_test("every day", tests.helpers.get_task_text_en)
