import tests.helpers
import todozer.scheduler
import todozer.utils


def run_test(pattern: str, task_text_function):

    today = todozer.utils.get_date_of_today()

    # If there is no start date at all:

    task_text = task_text_function(pattern)

    assert todozer.scheduler.match(task_text, today) is True

    # If start date is yesterday:

    task_date = todozer.utils.get_date_of_yesterday()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, today) is True

    # If start date is today:

    task_date = today
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, today) is True

    # If start date is tomorrow:

    task_date = todozer.utils.get_date_of_tomorrow()
    task_text = task_text_function(pattern, task_date)

    assert todozer.scheduler.match(task_text, today) is False


def test_every_day():

    run_test("каждый день", tests.helpers.get_task_text_ru)
    run_test("every day", tests.helpers.get_task_text_en)
