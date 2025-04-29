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
    dictionary,
    title="",
    key="Keys",
    value="Values",
    table_options: dict = None,
    key_options: dict = None,
    value_options: dict = None,
) -> Table:
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


def print_args(args) -> Table:
    result = print_table(args, title="Running Arguments", key="Arguments")
    return result
