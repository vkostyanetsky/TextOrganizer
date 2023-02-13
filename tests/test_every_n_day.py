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

    debug_code = tests.helpers.get_debug_code(plan.title_line, today)
    matched_pattern, is_date_matched = match(plan, today)
    assert matched_pattern is Pattern.EVERY_N_DAY and is_date_matched, debug_code

    debug_code = tests.helpers.get_debug_code(plan.title_line, three_days_after)
    matched_pattern, is_date_matched = match(plan, three_days_after)
    assert matched_pattern is Pattern.EVERY_N_DAY and is_date_matched, debug_code

    debug_code = tests.helpers.get_debug_code(plan.title_line, seven_days_after)
    matched_pattern, is_date_matched = match(plan, seven_days_after)
    assert matched_pattern is Pattern.EVERY_N_DAY and not is_date_matched, debug_code

    # en

    plan = tests.helpers.get_plan_en("every 3 days", today)

    debug_code = tests.helpers.get_debug_code(plan.title_line, today)
    matched_pattern, is_date_matched = match(plan, today)
    assert matched_pattern is Pattern.EVERY_N_DAY and is_date_matched, debug_code

    debug_code = tests.helpers.get_debug_code(plan.title_line, three_days_after)
    matched_pattern, is_date_matched = match(plan, three_days_after)
    assert matched_pattern is Pattern.EVERY_N_DAY and is_date_matched, debug_code

    debug_code = tests.helpers.get_debug_code(plan.title_line, seven_days_after)
    matched_pattern, is_date_matched = match(plan, seven_days_after)
    assert matched_pattern is Pattern.EVERY_N_DAY and not is_date_matched, debug_code
