#!/usr/bin/env python3

import click

from todozer.mode import ding, plan, test, view


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

    if mode == "plan":
        plan.main(path)
    elif mode == "test":
        test.main(path)
    elif mode == "view":
        view.main(path)
    elif mode == "ding":
        ding.main(path)
