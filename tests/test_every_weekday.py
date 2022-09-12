import tests.helpers
import todozer.utils
from todozer.scheduler import Pattern, match


def test_every_month():

    run_test(
        [
            "по будням",
            "по будним дням",
            "каждый будний день",
        ],
        tests.helpers.get_plan_ru,
    )

    run_test(
        [
            "weekdays",
            "every weekday",
        ],
        tests.helpers.get_plan_en,
    )


def run_test(variants: list, plan_function):

    monday = tests.helpers.get_day_of_week(0)
    before_monday = todozer.utils.get_date_of_yesterday(monday)
    after_monday = todozer.utils.get_date_of_tomorrow(monday)

    sunday = tests.helpers.get_day_of_week(6)
    before_sunday = todozer.utils.get_date_of_yesterday(sunday)
    after_sunday = todozer.utils.get_date_of_tomorrow(sunday)

    for variant in variants:

        task_text = tests.helpers.get_plan_ru(variant)
        assert match(task_text, monday) is Pattern.EVERY_WEEKDAY

        task_text = tests.helpers.get_plan_ru(variant, before_monday)
        assert match(task_text, monday) is Pattern.EVERY_WEEKDAY

        task_text = tests.helpers.get_plan_ru(variant, monday)
        assert match(task_text, monday) is Pattern.EVERY_WEEKDAY

        task_text = tests.helpers.get_plan_ru(variant, after_monday)
        assert match(task_text, monday) is not Pattern.EVERY_WEEKDAY

        task_text = tests.helpers.get_plan_ru(variant)
        assert match(task_text, sunday) is not Pattern.EVERY_WEEKDAY

        task_text = tests.helpers.get_plan_ru(variant, before_sunday)
        assert match(task_text, sunday) is not Pattern.EVERY_WEEKDAY

        task_text = tests.helpers.get_plan_ru(variant, sunday)
        assert match(task_text, sunday) is not Pattern.EVERY_WEEKDAY

        task_text = tests.helpers.get_plan_ru(variant, after_sunday)
        assert match(task_text, sunday) is not Pattern.EVERY_WEEKDAY
