#!/usr/bin/env python3

from todozer import browser, task_lists, utils


def main(path: str = None) -> None:
    """
    Opens tasks browser for current date.
    """

    config = utils.get_config(path)
    utils.set_logging(config)

    tasks_file_items = task_lists.load_tasks_file_items(config, path)
    plans_file_items = task_lists.load_plans_file_items(config, path)

    browser.TasksBrowser(tasks_file_items, plans_file_items).open()


if __name__ == "__main__":
    main()
