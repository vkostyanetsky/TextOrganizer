import datetime

import tests.helpers
import todozer.scheduler
import todozer.utils
import todozer.utils

def text_ru(day: str | int, start_date: datetime.date | None = None):
    return tests.helpers.get_task_text_ru(f"каждый месяц, {day} день", start_date)


def text_en(day: str | int, start_date: datetime.date | None = None):
    return tests.helpers.get_task_text_en(f"every month, {day} day", start_date)


def run_test(date: datetime.date, text_function):

    yesterday = date - datetime.timedelta(days=1)
    tomorrow = date + datetime.timedelta(days=1)

    # The task date is today, but we try to match it yesterday:

    task_text = text_function(date.day)
    assert todozer.scheduler.match(task_text, yesterday) is False

    # The task date is today:

    task_text = text_function(date.day)
    assert todozer.scheduler.match(task_text, date) is True

    # The task date is today, and it starts yesterday:

    task_text = text_function(date.day, yesterday)
    assert todozer.scheduler.match(task_text, date) is True

    # The task date is today, and it starts today:

    task_text = text_function(date.day, date)
    assert todozer.scheduler.match(task_text, date) is True

    # The task date is today, and it starts tomorrow:

    task_text = text_function(date.day, tomorrow)
    assert todozer.scheduler.match(task_text, date) is False


def test_every_month():

    this_day = todozer.utils.get_date_of_today()
    last_day = todozer.utils.get_month_last_day_date(this_day)

    # ru

    run_test(this_day, text_ru)
    run_test(last_day, text_ru)

    # en

    run_test(this_day, text_en)
    run_test(last_day, text_en)
