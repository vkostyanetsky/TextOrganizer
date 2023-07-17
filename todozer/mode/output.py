#!/usr/bin/env python3

"""Simply outputs tasks for a given date and quits."""

import click
from vkostyanetsky import cliutils

from todozer import utils


def main(path: str = None) -> None:
    """
    Checks plans file for errors.
    """

    config = utils.get_config(path)
    utils.set_logging(config)

    click.echo("oh hi mark")
    click.echo()

    cliutils.ask_for_enter()


if __name__ == "__main__":
    main()
