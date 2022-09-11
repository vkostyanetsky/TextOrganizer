import tests.helpers
import todozer.scheduler
import todozer.utils


def test_exact_date():

    yesterday = todozer.utils.get_date_of_yesterday()
    today = todozer.utils.get_date_of_today()
    tomorrow = todozer.utils.get_date_of_tomorrow()

    # If an exact date is yesterday:

    plan_date = todozer.utils.get_string_from_date(yesterday)
    plan = tests.helpers.get_plan_en(plan_date)

    assert todozer.scheduler.match(plan, today) is False

    # If an exact date is today:

    plan_date = todozer.utils.get_string_from_date(today)
    plan = tests.helpers.get_plan_en(plan_date)

    assert todozer.scheduler.match(plan, today) is True

    # If an exact date is tomorrow:

    plan_date = todozer.utils.get_string_from_date(tomorrow)
    plan = tests.helpers.get_plan_en(plan_date)

    assert todozer.scheduler.match(plan, today) is False
