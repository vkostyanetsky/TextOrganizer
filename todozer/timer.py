#!/usr/bin/env python3

"""
Functions to work with the tasks log file (timer.yaml by default).
"""

import os.path

import yaml
import yaml.parser
from datetime import datetime
from dataclasses import dataclass


def read() -> list:
    """
    Reads records from the file.
    """

    yaml_file_name = __get_file_name()

    result = []

    if os.path.isfile(yaml_file_name):

        try:

            with open(yaml_file_name, encoding="utf-8-sig") as yaml_file:
                result = yaml.safe_load(yaml_file)
                if result is None:
                    result = []

        except yaml.parser.ParserError:

            print(f"Unable to parse: {yaml_file_name}")

    return result


def write(logs: list[dict]) -> None:
    """
    Writes given logs to the log file.
    """

    __remove_microseconds(logs)

    yaml_file_name = __get_file_name()

    with open(yaml_file_name, encoding="utf-8-sig", mode="w") as yaml_file:
        yaml.safe_dump(logs, yaml_file)


def __get_file_name() -> str:
    """
    Returns a name for the log file.
    """

    return "timer.yaml"


def __remove_microseconds(records: list[dict]):
    """
    Removes microseconds from every log.
    """

    for record in records:

        record["started"] = record["started"].replace(microsecond=0)

        if record.get("stopped") is not None:
            record["stopped"] = record["stopped"].replace(microsecond=0)
