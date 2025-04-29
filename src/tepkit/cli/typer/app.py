import sys

import typer
from tepkit import __version__, package_root
from tepkit.cli import logger
from tepkit.cli.typer.docstring_to_typer import docstring_to_typer
from tepkit.cli.typer.utils import AliasGroup

# 获取配置信息
from tepkit.config import get_config

config = get_config()

# 修改默认 metavar
from click.types import IntParamType

IntParamType.name = "int"

# 创建 Typer 对象
app0 = typer.Typer()
app = typer.Typer(
    cls=AliasGroup,
    context_settings={"help_option_names": ["-h", "--help"]},  # 给帮助增加 -h 选项
    add_completion=config["typer"]["add_completion"],
    invoke_without_command=config["typer"]["invoke_without_command"],
    pretty_exceptions_enable=config["typer"]["pretty_exceptions_enable"],
    pretty_exceptions_show_locals=config["typer"]["pretty_exceptions_show_locals"],
    rich_markup_mode="rich",
)


@docstring_to_typer
@app0.callback(invoke_without_command=True)
def app0_callback(
    # context: typer.Context,
    test: list[str],
    version: bool = False,
    whereis: bool = False,
    log_level: str = "",
):
    """
    :typer version flag: --version, -v
    :typer whereis flag: --where, -w
    :typer test argument:
    """
    _ = version, whereis, log_level
    return test[0]


# 主命令接收参数的处理
@docstring_to_typer
@app.callback()
def root(
    context: typer.Context,
    version: bool = False,
    whereis: bool = False,
    log_level: str = config["loguru"]["log_level"],
):
    """
    Welcome to Tepkit!
    [bright_black]Note: The command number (c__) may change with the version,
    please use the full name when using tepkit in your script.[/]


    :param context  : The typer context object.
    :param version  : Show the version of Tepkit.
    :param whereis  : Show the path of Tepkit package.
    :param log_level: Set the log level of current execution.

    :typer version flag: --version, -v
    :typer whereis flag: --where, -w

    :typer log_level metavar: LEVEL
    """
    # subcommand: str = context.invoked_subcommand
    # 配置 log 等级
    log_level = int(log_level) if log_level.isdigit() else log_level
    logger.remove()
    logger.add(
        sys.stdout,
        format=config["loguru"]["format"],
        level=log_level,
    )
    logger.debug(f"Current log level: {log_level}")
    # 处理其他参数
    if version:  # 显示程序版本
        print(__version__)
    if whereis:  # 显示软件包路径
        print(package_root)
    if len(sys.argv) == 1:  # 如果没有任何子命令
        print("===== Tepkit Info =====")
        print(" Version :", __version__)
        print(" Location:", package_root)
        print("===== Tepkit Help =====")
        print(context.get_help())
        # print("Please use -h or --help to show help.")


@docstring_to_typer
def custom_warning(ignore: bool = False):
    """
    Print a warning message when running a custom command.

    :param ignore: ignore the warning message for custom commands.
    :typer ignore flag: --ignore-warning, -i
    """
    if ignore:
        return

    from rich import print
    from rich.panel import Panel

    title = "[bold bright_yellow]WARNING[/bold bright_yellow]"
    warning_text = [
        "[yellow]"
        + "Tepkit only provides an interface and do not assume any responsibility for your custom scripts.",
        "Please make sure you fully understand the function of your custom commands you are executing."
        + "[/yellow]",
        "(Use `custom -i` to disable this message)",
    ]
    panel = Panel(
        "\n".join(warning_text),
        title=title,
        border_style="yellow",
        title_align="left",
    )
    print(panel)
