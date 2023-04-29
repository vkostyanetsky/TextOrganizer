#!/usr/bin/env python3

import argparse
import configparser
import logging
import os.path
import sys

from vkostyanetsky import cliutils

from todozer import app_plans, app_tasks, constants, state_file


def main():
    """
    Main entry point of the application.
    """

    arguments = get_arguments()

    config = get_config(arguments.config)
    state = state_file.load()

    if config.getboolean("LOG", "write_log"):
        logging.basicConfig(
            filename=config.get("LOG", "file_name"),
            filemode=config.get("LOG", "file_mode"),
            encoding=constants.ENCODING,
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=logging.DEBUG,
            force=True,
        )

    session = {"config": config, "state": state}

    main_menu(session)


def main_menu(session: dict) -> None:
    """
    Displays the main menu of the application.
    """

    menu = cliutils.Menu([constants.TITLE])

    menu.add_item("View Tasks", app_tasks.main_menu, session)
    menu.add_item("Plan Tasks", app_plans.main_menu, session)

    menu.add_item_separator()

    menu.add_item("Exit", sys.exit)

    menu.choose()


def get_arguments() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(description="TODOZER KNOWS THE DRILL!")

    args_parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="todozer.cfg",
        help="configuration file name (default: todozer.cfg)",
    )

    return args_parser.parse_args()


def get_config(filename: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()

    config.read_dict(
        {
            "TASKS": {
                "file_name": "tasks.md",
                "reverse_days_order": False,
            },
            "PLANS": {
                "file_name": "plans.md",
            },
            "LOG": {"write_log": False, "file_name": "todozer.log", "file_mode": "w"},
        }
    )

    if os.path.exists(filename):
        config.read(filename, encoding=constants.ENCODING)
    else:
        with open(filename, "w", encoding=constants.ENCODING) as file:
            config.write(file)

    return config
