import yaml
from yaml.parser import ParserError


def save_yaml(file_name: str, file_data: dict) -> None:

    with open(yaml_file_name, encoding="utf-8-sig", mode="w") as yaml_file:
        safe_dump(file_data, yaml_file)


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
