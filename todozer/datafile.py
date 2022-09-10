import os
from todozer import utils

import yaml
from yaml.parser import ParserError


def __save_yaml(file_name: str, file_data: dict) -> None:

    with open(file_name, encoding="utf-8", mode="w") as yaml_file:
        yaml.safe_dump(file_data, yaml_file)


def __load_yaml(file_name: str) -> dict:

    result = None

    try:

        with open(file_name, encoding="utf-8") as yaml_file:
            result = yaml.safe_load(yaml_file)

    except ParserError:
        print(f"Unable to parse {file_name}!")

    if result is None:
        result = {}

    return result


def __get_data_by_default() -> dict:

    last_date = utils.get_date_of_yesterday()

    return {"last_date": last_date}


def __get_data_file_name() -> str:

    return "todozer.dat"


def load() -> dict:

    file_name = __get_data_file_name()

    return __load_yaml(file_name) if os.path.exists(file_name) else __get_data_by_default()


def save(data: dict):

    file_name = __get_data_file_name()

    __save_yaml(file_name, data)
