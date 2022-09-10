import tests.helpers
import todozer.scheduler
import todozer.utils


def test_exact_date():

    yesterday = todozer.utils.get_date_of_yesterday()
    today = todozer.utils.get_date_of_today()
    tomorrow = todozer.utils.get_date_of_tomorrow()

    # If an exact date is yesterday:

    task_date = todozer.utils.get_string_from_date(yesterday)
    task_text = tests.helpers.get_task_text_en(task_date)

    assert todozer.scheduler.match(task_text, today) is False

    # If an exact date is today:

    task_date = todozer.utils.get_string_from_date(today)
    task_text = tests.helpers.get_task_text_en(task_date)

    assert todozer.scheduler.match(task_text, today) is True

    # If an exact date is tomorrow:

    task_date = todozer.utils.get_string_from_date(tomorrow)
    task_text = tests.helpers.get_task_text_en(task_date)

    assert todozer.scheduler.match(task_text, today) is False
