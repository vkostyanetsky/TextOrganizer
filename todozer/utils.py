import datetime

import yaml
from yaml.parser import ParserError


def save_yaml(file_name: str, file_data: dict) -> None:

    with open(file_name, encoding="utf-8-sig", mode="w") as yaml_file:
        yaml.safe_dump(file_data, yaml_file)


def load_yaml(file_name: str) -> dict:

    result = None

    try:

        with open(file_name, encoding="utf-8-sig") as yaml_file:
            result = yaml.safe_load(yaml_file)

    except ParserError:
        print(f"Unable to parse {file_name}!")

    if result is None:
        result = {}

    return result


def get_date_from_string(source: str) -> datetime.date:

    return datetime.datetime.strptime(source, "%Y-%m-%d").date()


def get_string_from_date(source: datetime.date) -> str:

    return source.strftime("%Y-%m-%d")


def get_month_last_day_date(date: datetime.date) -> datetime.date:

    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)
