import datetime

import tests.helpers
import todozer.scheduler
import todozer.utils


def run_test(date: datetime.date):

    day_before_date = date - datetime.timedelta(days=1)
    day_after_date = date + datetime.timedelta(days=1)

    # wrong day

    task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {date.day} день")
    assert todozer.scheduler.match(task_text, day_before_date) is False

    # right day

    task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {date.day} день")
    assert todozer.scheduler.match(task_text, date) is True

    # this day, started today

    task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {date.day} день", date)
    assert todozer.scheduler.match(task_text, date) is True

    # this day, started yesterday

    task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {date.day} день", day_before_date)
    assert todozer.scheduler.match(task_text, date) is True

    # this day, stars tomorrow

    task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {date.day} день", day_after_date)
    assert todozer.scheduler.match(task_text, date) is False


def test_every_month():

    today = tests.helpers.get_today_date()
    run_test(today)

    #
    # tomorrow = tests.helpers.get_tomorrow_date(today)
    # yesterday = tests.helpers.get_yesterday_date(today)
    #
    # not_today = (
    #     tests.helpers.get_tomorrow_date(today)
    #     if today.day == 1
    #     else tests.helpers.get_yesterday_date(today)
    # )
    # final_day = todozer.utils.get_month_last_day_date(today)

    # # not this day
    #
    # task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {not_today.day} день")
    # assert todozer.scheduler.match(task_text, today) is False
    #
    # # this day
    #
    # task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {today.day} день")
    # assert todozer.scheduler.match(task_text, today) is True
    #
    # # this day, started today
    #
    # task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {today.day} день", today)
    # assert todozer.scheduler.match(task_text, today) is True
    #
    # # this day, started yesterday
    #
    # task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {today.day} день", yesterday)
    # assert todozer.scheduler.match(task_text, today) is True
    #
    # # this day, stars tomorrow
    #
    # task_text = tests.helpers.get_task_text_ru(f"каждый месяц, {today.day} день", tomorrow)
    # assert todozer.scheduler.match(task_text, today) is False

    # # last day of month
    #
    # task_text = tests.helpers.get_task_text_ru("каждый месяц, последний день")
    # assert todozer.scheduler.match(task_text, final_day) is True
    #
    # # last day of month (wrong day to check)
    #
    # task_text = tests.helpers.get_task_text_ru("каждый месяц, последний день")
    # assert (
    #     todozer.scheduler.match(task_text, final_day - datetime.timedelta(days=1))
    #     is False
    # )
