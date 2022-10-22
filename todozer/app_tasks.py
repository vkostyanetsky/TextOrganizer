#!/usr/bin/env python3

from vkostyanetsky import cliutils

from todozer import app


def main_menu(session: dict) -> None:

    cliutils.ask_for_enter()

    app.main_menu(session)
