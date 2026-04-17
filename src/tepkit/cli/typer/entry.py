import sys
from importlib import import_module

import typer
from typer import rich_utils
from tepkit.cli import logger
from tepkit.cli.typer.app import app
from tepkit.cli.typer.commands_data import builtin_commands_data, builtin_groups_data
from tepkit.cli.typer.docstring_to_typer import docstring_to_typer
from tepkit.cli.typer.utils import AliasGroup

ROOT_HELP_FLAGS = {"-h", "--help", "--install-completion", "--show-completion"}
ROOT_OPTION_FLAGS = {"-v", "--version", "-w", "--where"}
ROOT_OPTION_FLAGS_WITH_VALUE = {"--log-level"}


def get_requested_subcommand(argv: list[str]) -> str | None:
    """
    Return the first top-level subcommand.
    """
    skip_next = False
    for arg in argv[1:]:
        if skip_next:
            skip_next = False
            continue
        if arg in ROOT_HELP_FLAGS:
            return None
        if arg.startswith("--log-level="):
            continue
        if arg in ROOT_OPTION_FLAGS_WITH_VALUE:
            skip_next = True
            continue
        if arg in ROOT_OPTION_FLAGS:
            continue
        if arg.startswith("-"):
            return None
        return arg
    return None


def add_commands_to_app(
    target,
    commands: list[dict],
    parent_group_module: str = None,
):
    for command in commands:
        command_name = " | ".join(command["command_names"])
        module_path = command.get("function_module", parent_group_module)
        module = import_module(module_path)
        function = getattr(module, command["function_name"])
        processed_function = docstring_to_typer(function)
        command_kwargs = command.get("kwargs", {})
        command_kwargs["rich_help_panel"] = command.get("command_panel", "Functions")
        target.command(command_name, **command_kwargs)(processed_function)


def add_groups_to_app(
    target,
    groups: list[dict],
    parent_group_module: str = None,
    skip_add_commands: bool = False,
):
    results = []
    for group in groups:
        # Prase
        group_name = " | ".join(group["group_names"])
        group_help = group.get("group_help", "")
        group_module = group.get("group_module", None) or parent_group_module
        sub_grouops = group.get("sub_groups", [])
        sub_commands = group.get("sub_commands", [])
        group_kwargs = group.get("kwargs", {})
        # Create Group
        this_app = typer.Typer(
            cls=AliasGroup,
            no_args_is_help=True,
            invoke_without_command=True,
            **group_kwargs,
        )
        # Add Group to Parent
        target.add_typer(
            this_app,
            name=group_name,
            help=group_help,
        )
        results.append(this_app)
        # Add Sub Groups and Commands
        add_groups_to_app(this_app, sub_grouops, parent_group_module=group_module)
        if not skip_add_commands:
            add_commands_to_app(
                this_app, sub_commands, parent_group_module=group_module
            )
    return results


def adjust_typer():
    rich_utils.STYLE_HELPTEXT = ""
    rich_utils.STYLE_OPTIONS_PANEL_BORDER = ""
    rich_utils.STYLE_COMMANDS_PANEL_BORDER = ""
    rich_utils.STYLE_OPTION_DEFAULT = "bright_black"


def main():
    logger.debug("Starting Tepkit ...")
    groups_data = builtin_groups_data
    commands_data = builtin_commands_data
    skip_add_commands = False
    subcommand = None
    if len(sys.argv) == 1:
        skip_add_commands = True
    else:
        subcommand = get_requested_subcommand(sys.argv)
        if subcommand is not None:
            # print(subcommand)
            for group in groups_data:
                if subcommand in group["group_names"]:
                    logger.debug(f"Subcommand found: {subcommand}")
                    groups_data = [group]
                    commands_data = []
                    break
            else:
                logger.debug(f"Unknown subcommand: {subcommand}")
    sub_apps = add_groups_to_app(app, groups_data, skip_add_commands=skip_add_commands)
    add_commands_to_app(app, commands_data)
    if subcommand in ["c99", "custom"]:
        from tepkit.cli.typer.app import custom_warning
        from tepkit.functions.custom import custom_commands_data

        custom_app = sub_apps[-1]
        add_commands_to_app(custom_app, custom_commands_data)
        custom_app.callback(invoke_without_command=True)(custom_warning)
    adjust_typer()
    app(windows_expand_args=False)


if __name__ == "__main__":
    main()
