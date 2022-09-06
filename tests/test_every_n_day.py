import datetime

import tests.helpers
import todozer.scheduler


def test_every_n_day():

    today = tests.helpers.get_today_date()

    three_days_after = today + datetime.timedelta(days=3)
    seven_days_after = today + datetime.timedelta(days=7)

    # ru

    task_text = tests.helpers.get_task_text_ru("каждые 3 дня", today)

    assert todozer.scheduler.match(task_text, today) is True
    assert todozer.scheduler.match(task_text, three_days_after) is True
    assert todozer.scheduler.match(task_text, seven_days_after) is False

    # en

    task_text = tests.helpers.get_task_text_en("every 3 days", today)

    assert todozer.scheduler.match(task_text, today) is True
    assert todozer.scheduler.match(task_text, three_days_after) is True
    assert todozer.scheduler.match(task_text, seven_days_after) is False
