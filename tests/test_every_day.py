import tests.helpers
import todozer.scheduler
import todozer.utils


def run_test(pattern: str, plan_function):

    today = todozer.utils.get_date_of_today()

    # If there is no start date at all:

    plan = plan_function(pattern)

    assert todozer.scheduler.match(plan, today) is True

    # If start date is yesterday:

    plan_date = todozer.utils.get_date_of_yesterday()
    plan = plan_function(pattern, plan_date)

    assert todozer.scheduler.match(plan, today) is True

    # If start date is today:

    plan_date = today
    plan = plan_function(pattern, plan_date)

    assert todozer.scheduler.match(plan, today) is True

    # If start date is tomorrow:

    plan_date = todozer.utils.get_date_of_tomorrow()
    plan = plan_function(pattern, plan_date)

    assert todozer.scheduler.match(plan, today) is False


def test_every_day():

    run_test("каждый день", tests.helpers.get_plan_ru)
    run_test("every day", tests.helpers.get_plan_en)
