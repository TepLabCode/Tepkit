from typing import NoReturn

from rich import print
from rich.panel import Panel
from rich.table import Table

PANEL_PRESETS = {
    "info": {
        "title_align": "left",
        "title": "Info",
        "border_style": "blue",
    },
    "warning": {
        "title_align": "left",
        "title": "Warning",
        "border_style": "yellow",
    },
    "error": {
        "title_align": "left",
        "title": "Error",
        "border_style": "red",
    },
}


def print_panel(content: str, preset: str = None, **kwargs) -> Panel:
    if preset is not None:
        preset = preset.lower()
        settings = PANEL_PRESETS[preset]
    else:
        settings = {}
    settings.update(kwargs)
    panel = Panel(str(content), **settings)
    print(panel)
    return panel


def print_table(
    dictionary: dict,
    title: str = "",
    key: str = "Keys",
    value: str = "Values",
    table_options: dict = None,
    key_options: dict = None,
    value_options: dict = None,
) -> Table:
    """
    A function to easily print a dict as a Rich table.

    :param dictionary:
    :param title:
    :param key:
    :param value:
    :param table_options:
    :param key_options:
    :param value_options:
    :return:
    """
    table_options = table_options or dict()
    key_options = key_options or dict()
    value_options = value_options or dict()
    table = Table(title=title, **table_options)
    table.add_column(key, **key_options)
    table.add_column(value, **value_options)
    for key, value in dictionary.items():
        table.add_row(str(key), str(value))
    print(table)
    return table


class TablePrinter:
    def __init__(
        self,
        title: str = "",
        key: str = "Keys",
        value: str = "Values",
        table_options: dict = None,
        key_options: dict = None,
        value_options: dict = None,
    ):
        """
        A class wapper for print_table function, avoiding pass the same arguments repeatedly.
        """
        self.title = title
        self.key = key
        self.value = value
        self.table_options = table_options or {}
        self.key_options = key_options or {}
        self.value_options = value_options or {}

    def print(
        self,
        dictionary=None,
        title=None,
        key=None,
        value=None,
    ):
        return print_table(
            dictionary=dictionary,
            title=title or self.title,
            key=key or self.key,
            value=value or self.value,
            table_options=self.table_options,
            key_options=self.key_options,
            value_options=self.value_options,
        )


def print_args(args) -> Table:
    result = print_table(args, title="Running Arguments", key="Arguments")
    return result
