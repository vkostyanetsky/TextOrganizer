import datetime

from todozer import scheduler
from todozer import utils


def match(task_text: str) -> bool:
    today = get_today_date()

    return scheduler.match(task_text, today)


def get_task_text(pattern: str) -> str:
    return f'* Bob, do something!; {pattern}'


def get_yesterday_date() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)


def get_today_date() -> datetime.date:
    return datetime.date.today()


def get_tomorrow_date() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=1)


def get_task_text_with_start_date_in_russian(pattern: str, start_date: datetime.date) -> str:
    text = get_task_text(pattern)
    date = utils.get_string_from_date(start_date)

    return f'{text} с {date}'


def get_task_text_with_start_date_in_english(pattern: str, start_date: datetime.date) -> str:
    text = get_task_text(pattern)
    date = utils.get_string_from_date(start_date)

    return f'{text} from {date}'


def test_exact_date_yesterday():
    task_date = utils.get_string_from_date(get_yesterday_date())
    task_text = get_task_text(task_date)

    assert match(task_text) is False


def test_exact_date_today():
    task_date = utils.get_string_from_date(get_today_date())
    task_text = get_task_text(task_date)

    assert match(task_text) is True


def test_exact_date_tomorrow():
    task_date = utils.get_string_from_date(get_tomorrow_date())
    task_text = get_task_text(task_date)

    assert match(task_text) is False


def test_every_day_ru():
    task_text = get_task_text('каждый день')

    assert match(task_text) is True


def test_every_day_ru_with_start_date_yesterday():
    task_date = get_yesterday_date()
    task_text = get_task_text_with_start_date_in_russian('каждый день', task_date)

    assert match(task_text) is True


def test_every_day_ru_with_start_date_today():
    task_date = get_today_date()
    task_text = get_task_text_with_start_date_in_russian('каждый день', task_date)

    assert match(task_text) is True


def test_every_day_ru_with_start_date_tomorrow():
    task_date = get_tomorrow_date()
    task_text = get_task_text_with_start_date_in_russian('каждый день', task_date)

    assert match(task_text) is True


def test_every_day_en():
    task_text = get_task_text('every day')

    assert match(task_text) is True


def test_every_day_en_with_start_date_yesterday():
    task_date = get_yesterday_date()
    task_text = get_task_text_with_start_date_in_english('every day', task_date)

    assert match(task_text) is True


def test_every_day_en_with_start_date_today():
    task_date = get_today_date()
    task_text = get_task_text_with_start_date_in_english('every day', task_date)

    assert match(task_text) is True


def test_every_day_en_with_start_date_tomorrow():
    task_date = get_tomorrow_date()
    task_text = get_task_text_with_start_date_in_english('every day', task_date)

    assert match(task_text) is False
