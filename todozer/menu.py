#!/usr/bin/env python3

from vkostyanetsky import cliutils


class OrganizerMenu(cliutils.Menu):
    def _print_menu(self):

        print(self._top_border())

        self._print_title()

        self._print_choices()

        print(self._bottom_border())

    def _print_title(self):

        print(self._text_line("FASTING TIMER", 2))

        print(self._inner_border())

    def _print_choices(self):

        print(self._empty_line())

        for choice in self._get_choices_to_print():
            print(self._text_line(text=choice))

        print(self._empty_line())

    def print(self):
        """
        Draws the menu.
        """
        print()

        self._print_menu()

        print(self._prompt, end="")
