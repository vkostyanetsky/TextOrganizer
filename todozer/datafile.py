import os

import yaml
from yaml.parser import ParserError

from todozer import constants, utils


def save_yaml(file_name: str, file_data: dict) -> None:

    with open(file_name, encoding=constants.encoding, mode="w") as yaml_file:
        yaml.safe_dump(file_data, yaml_file)


def load_yaml(file_name: str) -> dict:

    result = None

    try:

        with open(file_name, encoding=constants.encoding) as yaml_file:
            result = yaml.safe_load(yaml_file)

    except ParserError:
        print(f"Unable to parse {file_name}!")

    if result is None:
        result = {}

    return result


def get_data_file_name() -> str:

    return "todozer.dat"


def get_data_by_default() -> dict:

    return {"last_date": utils.get_date_of_yesterday()}


def load() -> dict:

    file_name = get_data_file_name()

    return load_yaml(file_name) if os.path.exists(file_name) else get_data_by_default()


def save(data: dict):

    file_name = get_data_file_name()

    save_yaml(file_name, data)
