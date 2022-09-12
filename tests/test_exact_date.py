import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def test_exact_date():

    yesterday = todozer.utils.get_date_of_yesterday()
    today = todozer.utils.get_date_of_today()
    tomorrow = todozer.utils.get_date_of_tomorrow()

    # If an exact date is yesterday:

    plan_date = todozer.utils.get_string_from_date(yesterday)
    plan = tests.helpers.get_plan_en(plan_date)

    assert match(plan, today) is not Pattern.EXACT_DATE

    # If an exact date is today:

    plan_date = todozer.utils.get_string_from_date(today)
    plan = tests.helpers.get_plan_en(plan_date)

    assert match(plan, today) is Pattern.EXACT_DATE

    # If an exact date is tomorrow:

    plan_date = todozer.utils.get_string_from_date(tomorrow)
    plan = tests.helpers.get_plan_en(plan_date)

    assert match(plan, today) is not Pattern.EXACT_DATE
