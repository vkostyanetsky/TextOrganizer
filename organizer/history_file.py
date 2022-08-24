from yaml import safe_dump as write_yaml
from yaml import safe_load as parse_yaml

import yaml
from yaml.parser import ParserError


class HistoryFile:
    __file_path: str
    dates: list

    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path

        self.dates = []

    def load(self) -> None:
        try:

            with open(self.__file_path, encoding="utf-8-sig") as yaml_file:
                content = yaml.safe_load(yaml_file)

            self.dates = content["dates"]

        except FileNotFoundError:
            print(f"{self.__file_path} is not found!")

        except ParserError:
            print(f"Unable to parse {self.__file_path}!")

    def save(self) -> None:
        yaml.safe_dump({"dates": self.dates})
