import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def test_exact_date():

    yesterday = todozer.utils.get_date_of_yesterday()
    tomorrow = todozer.utils.get_date_of_tomorrow()
    today = todozer.utils.get_date_of_today()

    # If an exact date is yesterday:

    plan_date = todozer.utils.get_string_from_date(yesterday)
    plan = tests.helpers.get_plan_en(plan_date)
    matched_pattern, is_date_matched = match(plan, today)

    assert matched_pattern is Pattern.EXACT_DATE and not is_date_matched

    # If an exact date is today:

    plan_date = todozer.utils.get_string_from_date(today)
    plan = tests.helpers.get_plan_en(plan_date)
    matched_pattern, is_date_matched = match(plan, today)

    assert matched_pattern is Pattern.EXACT_DATE and is_date_matched

    # If an exact date is tomorrow:

    plan_date = todozer.utils.get_string_from_date(tomorrow)
    plan = tests.helpers.get_plan_en(plan_date)
    matched_pattern, is_date_matched = match(plan, today)

    assert matched_pattern is Pattern.EXACT_DATE and not is_date_matched
