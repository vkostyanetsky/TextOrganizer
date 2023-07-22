#!/usr/bin/env python3

import click

from sys import stdout

from todozer import constants
from todozer.commands import command_show, command_beep, command_make, command_test


def path_help() -> str:
    return "Path to working directory."


def path_type() -> click.Path:
    return click.Path(exists=True)


@click.group()
@click.option(
    "-p", "--path", type=path_type(), help=path_help()
)
def main(path: str):
    stdout.reconfigure(encoding=constants.ENCODING)


@main.command()
@click.option(
    "-p", "--path", type=path_type(), help=path_help()
)
def make(path: str) -> None:
    """
    Make planned tasks for a brand-new day.
    """

    command_make.main(path)


@main.command()
@click.option(
    "-p", "--path", type=path_type(), help=path_help()
)
def test(path: str) -> None:
    """
    Check that working directory has no mistakes.
    """
    command_test.main(path)


@main.command()
@click.option(
    "-p", "--path", type=path_type(), help=path_help()
)
def beep(path: str):
    """
    Set alarm according to notification settings.
    """
    command_beep.main(path)


@main.command()
@click.argument(
    "what", default="today", type=click.Choice(['today', 'last', 'next', 'date'])
)
@click.argument(
    "detail", default=""
)
@click.option(
    "-p", "--path", type=path_type(), help=path_help()
)
def show(path: str, what: str, detail: str):
    """
    Display tasks for a given day (or days).
    """
    command_show.main(what, detail, path)


if __name__ == '__main__':
    main()
