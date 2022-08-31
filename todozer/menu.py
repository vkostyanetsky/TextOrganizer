#!/usr/bin/env python3

"""
Contains a class which implements the main menu for the application.
"""

from vkostyanetsky import cliutils


class TodozerMenu(cliutils.Menu):
    """
    Class of the main menu. Intended to show app's title
    and a list of choices to pick.
    """

    def _print_title(self) -> None:
        """
        Displays the title of the application.
        """

        print(self._text_line("TODOZER", 2))

        print(self._inner_border())

    def _print_choices(self) -> None:
        """
        Displays the list of possible choices with a padding above and below.
        """

        print(self._empty_line())

        for choice in self._get_choices_to_print():
            print(self._text_line(text=choice))

        print(self._empty_line())

    def _print_menu(self):
        """
        Displays the menu.
        """

        print(self._top_border())

        self._print_title()

        self._print_choices()

        print(self._bottom_border())

    def print(self):
        """
        Displays the menu and a user's prompt.
        """

        print()

        self._print_menu()

        print(self._prompt, end="")
