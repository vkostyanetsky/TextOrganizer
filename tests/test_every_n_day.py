import datetime

import tests.helpers
import todozer.scheduler
import todozer.utils


def test_every_n_day():

    today = todozer.utils.get_date_of_today()

    three_days_after = today + datetime.timedelta(days=3)
    seven_days_after = today + datetime.timedelta(days=7)

    # ru

    plan = tests.helpers.get_plan_ru("каждые 3 дня", today)

    assert todozer.scheduler.match(plan, today) is True
    assert todozer.scheduler.match(plan, three_days_after) is True
    assert todozer.scheduler.match(plan, seven_days_after) is False

    # en

    plan = tests.helpers.get_plan_en("every 3 days", today)

    assert todozer.scheduler.match(plan, today) is True
    assert todozer.scheduler.match(plan, three_days_after) is True
    assert todozer.scheduler.match(plan, seven_days_after) is False
