import tests
import todozer.utils
import todozer.scheduler


def test_exact_date():

    yesterday = tests.get_yesterday_date()
    today = tests.get_today_date()
    tomorrow = tests.get_tomorrow_date()

    # If an exact date is yesterday:

    task_date = todozer.utils.get_string_from_date(yesterday)
    task_text = tests.get_task_text_en(task_date)

    assert todozer.scheduler.match(task_text, today) is False

    # If an exact date is today:

    task_date = todozer.utils.get_string_from_date(today)
    task_text = tests.get_task_text_en(task_date)

    assert todozer.scheduler.match(task_text, today) is True

    # If an exact date is tomorrow:

    task_date = todozer.utils.get_string_from_date(tomorrow)
    task_text = tests.get_task_text_en(task_date)

    assert todozer.scheduler.match(task_text, today) is False
