#!/usr/bin/env python3

from sys import stdout

import click

from todozer import constants
from todozer.commands import command_beep, command_make, command_show, command_test


def path_help() -> str:
    return "Set path to working directory."


def path_type() -> click.Path:
    return click.Path(exists=True)


@click.group(help="CLI tool to manage tasks & duties.")
@click.option("-p", "--path", type=path_type(), help=path_help())
def main(path: str):
    stdout.reconfigure(encoding=constants.ENCODING)


@main.command(help="Make planned tasks for a brand-new day.")
@click.option("-p", "--path", type=path_type(), help=path_help())
def make(path: str) -> None:
    command_make.main(path)


@main.command(help="Check that working directory has no mistakes.")
@click.option("-p", "--path", type=path_type(), help=path_help())
def test(path: str) -> None:
    command_test.main(path)


@main.command(help="Set alarm according to notification settings.")
@click.option("-p", "--path", type=path_type(), help=path_help())
def beep(path: str):
    command_beep.main(path)


@main.command(help="Display tasks for a given day (or days).")
@click.argument(
    "period", default="today", type=click.Choice(["today", "last", "next", "date"])
)
@click.argument("value", default="")
@click.option("-p", "--path", type=path_type(), help=path_help())
@click.option("-t", "--timesheet", is_flag=True, help="Show only tasks with time logged.")
def show(path: str, timesheet: bool, period: str, value: str):
    command_show.main(period, value, path, timesheet)


if __name__ == "__main__":
    main()
