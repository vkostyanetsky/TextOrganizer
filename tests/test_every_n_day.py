import datetime

import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def test_every_n_day():

    today = todozer.utils.get_date_of_today()

    three_days_after = today + datetime.timedelta(days=3)
    seven_days_after = today + datetime.timedelta(days=7)

    # ru

    plan = tests.helpers.get_plan_ru("каждые 3 дня", today)

    assert match(plan, today) is Pattern.EVERY_N_DAY
    assert match(plan, three_days_after) is Pattern.EVERY_N_DAY
    assert match(plan, seven_days_after) is not Pattern.EVERY_N_DAY

    # en

    plan = tests.helpers.get_plan_en("every 3 days", today)

    assert match(plan, today) is Pattern.EVERY_N_DAY
    assert match(plan, three_days_after) is Pattern.EVERY_N_DAY
    assert match(plan, seven_days_after) is not Pattern.EVERY_N_DAY
