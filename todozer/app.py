#!/usr/bin/env python3

import click

from todozer.mode import alarm, browse, check, create, output


@click.command()
@click.argument(
    "mode",
    type=click.Choice(
        ["create", "browse", "output", "check", "alarm"], case_sensitive=False
    ),
)
@click.option(
    "-p", "--path", type=click.Path(exists=True), help="Path to working directory."
)
def main(mode: str, path: str):
    """
    I know the drill!
    """

    if mode == "create":
        create.main(path)
    elif mode == "browse":
        browse.main(path)
    elif mode == "output":
        output.main(path)
    elif mode == "check":
        check.main(path)
    elif mode == "alarm":
        alarm.main(path)
