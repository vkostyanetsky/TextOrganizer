from yaml import safe_dump as write_yaml
from yaml import safe_load as parse_yaml
from yaml.parser import ParserError as YamlParserError


class HistoryFile:
    __file_path: str
    planned_dates: list

    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.planned_dates = []

    def load(self) -> None:
        try:

            with open(self.__file_path, encoding="utf-8-sig") as yaml_file:
                content = parse_yaml(yaml_file)

            self.planned_dates = content["planned_dates"]

        except FileNotFoundError:
            print(f"{self.__file_path} is not found!")

        except YamlParserError:
            print(f"Unable to parse {self.__file_path}!")

    def save(self) -> None:
        write_yaml({"planned_dates": self.planned_dates})
