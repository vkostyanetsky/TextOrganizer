#!/usr/bin/env python3

import configparser
import logging
import os.path

import click

from todozer import constants, state_file
from todozer.mode import test, plan, ding, view


@click.command()
@click.argument(
    "mode",
    type=click.Choice(["plan", "test", "view", "ding"], case_sensitive=False),
)
@click.option(
    "-p", "--path", type=click.Path(exists=True), help="Set path to working directory."
)
def main(mode: str, path: str):
    """
    I know the drill!
    """

    config = __get_config(path)

    __set_logging(config)

    if mode == "plan":
        plan.main(config, path)
    elif mode == "test":
        test.main(config, path)
    elif mode == "view":
        view.main(config, path)
    elif mode == "ding":
        ding.main(config, path)


def __set_logging(config) -> None:
    if config.getboolean("LOG", "write_log"):
        logging.basicConfig(
            filename=config.get("LOG", "file_name"),
            filemode=config.get("LOG", "file_mode"),
            encoding=constants.ENCODING,
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=logging.DEBUG,
            force=True,
        )


def __get_config(path: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()

    settings = {
        "TASKS": {
            "file_name": "tasks.md",
            "reverse_days_order": False,
        },
        "PLANS": {
            "file_name": "plans.md",
        },
        "LOG": {"write_log": False, "file_name": "todozer.log", "file_mode": "w"},
        "NOTIFICATIONS": {
            "future_days_number": 7,
            "telegram_bot_api_token": "",
            "telegram_chat_id": "",
        },
    }

    config.read_dict(settings)

    filename = "todozer.cfg"

    if path is not None:
        filename = os.path.join(path, filename)

    if os.path.exists(filename):
        config.read(filename, encoding=constants.ENCODING)
    else:
        with open(filename, "w", encoding=constants.ENCODING) as file:
            config.write(file)

    return config
