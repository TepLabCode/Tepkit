"""
Ref: https://matplotlib.org/stable/api/ticker_api.html
"""

from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from tepkit.utils.mpl_tools.formatters import get_decimal_formatter

# Locator

ticker_locators = {
    "auto": ticker.AutoLocator,
    "maxn": ticker.MaxNLocator,
    "linear": ticker.LinearLocator,
    "log": ticker.LogLocator,  # (base=10.0, subs=(1.0,), *, numticks=None)
    "multiple": ticker.MultipleLocator,
    "fixed": ticker.FixedLocator,
    "index": ticker.IndexLocator,
    "null": ticker.NullLocator,
    "symmetricallog": ticker.SymmetricalLogLocator,
    "asinh": ticker.AsinhLocator,
    "logit": ticker.LogitLocator,
    "autominor": ticker.AutoMinorLocator,
    # Alias
    "gap": ticker.MultipleLocator,
}


def set_axis_ticker_locator(
    axis: mpl.axis.Axis,
    locator: str,
    arg: Any = None,
    minor: bool = False,
):
    """
    Set the ticker locator of the given axis (ax.xaxis or ax.yaxis).
    """
    locator = locator.lower().replace("_", "")
    if not minor:
        set_locator = axis.set_major_locator
    else:
        set_locator = axis.set_minor_locator
    if locator == "half-log":
        set_locator(ticker.LogLocator(base=10.0, subs=(0.5,)))
        return
    match arg:
        case None:
            set_locator(ticker_locators[locator]())
        case dict():
            set_locator(ticker_locators[locator](**arg))
        case _:
            set_locator(ticker_locators[locator](arg))


def set_axes_ticker_locator(
    ax: mpl.axes.Axes,
    direction: str,
    locator: str,
    arg: Any = None,
    minor: bool = False,
):
    """
    Set the ticker locator of the given axes (ax).
    Usage:
    >>> set_axes_ticker_locator(ax, "x", "auto")
    >>> set_axes_ticker_locator(ax, "y", "log", {"base": 10})
    """
    direction = direction.lower()
    if direction not in ["x", "y", "both"]:
        raise ValueError("direction must be 'x', 'y', or 'both'.")
    if direction in ["x", "both"]:
        set_axis_ticker_locator(ax.xaxis, locator, arg, minor)
    if direction in ["y", "both"]:
        set_axis_ticker_locator(ax.yaxis, locator, arg, minor)


def set_ticker_locator(
    target: mpl.axis.Axis | mpl.axes.Axes,
    locator: str,
    arg: Any = None,
    minor: bool = False,
    direction: str = None,
):
    """
    Set the ticker locator of the given axis (ax.xaxis or ax.yaxis) or axes (ax).
    """
    if isinstance(target, mpl.axis.Axis):
        set_axis_ticker_locator(target, locator, arg, minor)
    elif isinstance(target, mpl.axes.Axes):
        set_axes_ticker_locator(target, direction, locator, arg, minor)
    else:
        raise ValueError("target must be an Axis or Axes object.")


# Formatter

ticker_formatters = {
    "null": ticker.NullFormatter,
    "fixed": ticker.FixedFormatter,
    "func": ticker.FuncFormatter,
    "strmethod": ticker.StrMethodFormatter,
    "formatstr": ticker.FormatStrFormatter,
    "scalar": ticker.ScalarFormatter,
    "log": ticker.LogFormatter,
    "logexponent": ticker.LogFormatterExponent,
    "logmathtext": ticker.LogFormatterMathtext,
    "logscinotation": ticker.LogFormatterSciNotation,
    "logit": ticker.LogitFormatter,
    "eng": ticker.EngFormatter,
    "percent": ticker.PercentFormatter,
}


def set_axis_ticker_formatter(
    axis: mpl.axis.Axis,
    formatter: str,
    arg: Any = None,
    minor: bool = False,
):
    """
    Set the ticker formatter of the given axis (ax.xaxis or ax.yaxis).
    """
    formatter = formatter.lower().replace("_", "")
    if not minor:
        set_formatter = axis.set_major_formatter
    else:
        set_formatter = axis.set_minor_formatter
    match arg:
        case None:
            set_formatter(ticker_formatters[formatter]())
        case dict():
            set_formatter(ticker_formatters[formatter](**arg))
        case _:
            set_formatter(ticker_formatters[formatter](arg))


def set_axes_ticker_formatter(
    ax: mpl.axes.Axes,
    direction: str,
    formatter: str,
    arg: Any = None,
    minor: bool = False,
):
    """
    Set the ticker formatter of the given axes (ax).
    Usage:
    >>> set_axes_ticker_formatter(ax, "x", "null")
    >>> set_axes_ticker_formatter(ax, "y", "log", {"base": 10})
    """
    direction = direction.lower()
    if direction not in ["x", "y", "both"]:
        raise ValueError("direction must be 'x', 'y', or 'both'.")
    if direction in ["x", "both"]:
        set_axis_ticker_formatter(ax.xaxis, formatter, arg, minor)
    if direction in ["y", "both"]:
        set_axis_ticker_formatter(ax.yaxis, formatter, arg, minor)


def set_ticker_formatter(
    target: mpl.axis.Axis | mpl.axes.Axes,
    formatter: str,
    direction: str = None,
    arg: Any = None,
    minor: bool = False,
):
    """
    Set the ticker formatter of the given axis (ax.xaxis or ax.yaxis) or axes (ax).
    """
    if isinstance(target, mpl.axis.Axis):
        set_axis_ticker_formatter(target, formatter, arg, minor)
    elif isinstance(target, mpl.axes.Axes):
        set_axes_ticker_formatter(target, direction, formatter, arg, minor)
    else:
        raise ValueError("target must be an Axis or Axes object.")


if __name__ == "__main__":

    def test():
        from tepkit.utils.mpl_tools import Figure

        mpl.use("TkAgg")
        figure = Figure()
        ax = figure.ax
        ax.plot([1, 2, 3], [1, 2, 3])
        set_axes_ticker_locator(ax, "x", "auto")
        set_axes_ticker_locator(ax, "y", "log", {"base": 10})
        set_axes_ticker_formatter(ax, "x", "null")
        set_axes_ticker_formatter(ax, "y", "log", {"base": 10})
        figure.show(dpi=200)

    test()
