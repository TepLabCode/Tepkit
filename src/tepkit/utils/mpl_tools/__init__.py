from matplotlib import pyplot as plt
from tepkit import package_root
from tepkit.utils.mpl_tools.ticker_tools import (
    set_axes_ticker_formatter,
    set_axes_ticker_locator,
)

style_dir = package_root / "utils/mpl_tools/styles"
style_path = {
    "default": "default",
    "tepkit_basic": style_dir / "tepkit_basic.mplstyle",
}


def adjust_legend_linewidth(ax, linewidth: float = None):
    if linewidth is None:
        axis_linewidths = [
            ax.spines[axis].get_linewidth()
            for axis in ["top", "bottom", "left", "right"]
        ]
        linewidth = sum(axis_linewidths) / 4
    ax.get_legend().get_frame().set_linewidth(linewidth)


class Figure:
    def __init__(
        self,
        width: float = 1.0,
        height: float = 0.9,
        # Additional Settings
        dpi: float = None,
        font_size=None,
        # Style
        style="tepkit_basic",
    ):
        plt.style.use(style_path[style.lower()])
        figsize = (3.334 * width, 3.334 * height)
        self.width: int | float = width
        """
        | The ratio to the recommended width (3.334 inch = 1000 px at 300 dpi ≈ 8.47 cm),
        | default set to 1.0.
        """
        self.height: int | float = height
        """
        | The ratio to the recommended height (3.334 inch = 1000 px at 300 dpi ≈ 8.47 cm),
        | default set to 0.9.
        """
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)

        self.legend = None
        """The latest legend added by ``.add_legend()``."""
        self.colorbar = None
        """The latest colorbar added by ``.add_colorbar()``."""
        if dpi is not None:
            self.fig.set_dpi(dpi)
        if font_size is not None:
            plt.rcParams.update({"font.size": font_size})  # 设置字体大小为12

    def add_legend(
        self,
        *args,
        border_width: int | float | None = None,
        **kwargs,
    ):
        """
        A wrapper of ``matplotlib.pyplot.legend()``.

        :return: ``matplotlib.legend.Legend``

        Features
        ========
        - Add parameter aliases:
            - ``font_size``: ``fontsize``
        - Add automatic behaviors:
            - Sync the border width of the legend to the left axis.
        - Add new parameters:
            - ``border_width``: Set the border width of the legend.
        """
        # Agument alias
        if "font_size" in kwargs:
            kwargs["fontsize"] = kwargs.pop("font_size")
        # Main
        self.legend = plt.legend(*args, **kwargs)
        # Adjust legend border width
        ax_linewidth = self.ax.spines["left"].get_linewidth()
        border_width = border_width or ax_linewidth
        self.legend.get_frame().set_linewidth(border_width)
        # Return
        return self.legend

    def add_colorbar(
        self,
        *args,
        width: int | float = 1,
        height: int | float = 1,
        border_width: int | float | None = None,
        **kwargs,
    ):
        """
        A wrapper of ``matplotlib.pyplot.colorbar()``.

        :return: ``matplotlib.colorbar.Colorbar``

        Features
        ========
        - Add automatic behaviors:
            - Sync the border width of the colorbar to the left axis.
        - Add new parameters:
            - ``width`` and ``height``: Change the size of the colorbar.
            - ``border_width``: Set the border width of the colorbar.
        """
        # Size
        shrink = kwargs.pop("shrink", 1)
        aspect = kwargs.pop("aspect", 20)
        kwargs["shrink"] = shrink * height
        kwargs["aspect"] = aspect * height / width
        # Main
        self.colorbar = plt.colorbar(*args, **kwargs)
        # Adjust colorbar border width
        ax_linewidth = self.ax.spines["left"].get_linewidth()
        border_width = border_width or ax_linewidth
        self.colorbar.outline.set_linewidth(border_width)
        # Return
        return self.colorbar

    @staticmethod
    def adjust_margin(
        *,
        # Border
        top=None,
        right=None,
        bottom=None,
        left=None,
        # Between
        wspace=None,
        hspace=None,
    ) -> None:
        """
        A wrapper of ``matplotlib.pyplot.subplots_adjust()``.

        Adjust the margin of the figure **in pixels**.
        """
        fig = plt.gcf()
        width = fig.get_figwidth() * fig.get_dpi()
        height = fig.get_figheight() * fig.get_dpi()
        if left is not None:
            left = left / width
        if right is not None:
            right = 1 - right / width
        if top is not None:
            top = 1 - top / height
        if bottom is not None:
            bottom = bottom / height
        if wspace is not None:
            wspace = wspace / width
        if hspace is not None:
            hspace = hspace / height
        plt.subplots_adjust(
            top=top,
            right=right,
            bottom=bottom,
            left=left,
            wspace=wspace,
            hspace=hspace,
        )

    def set_locator(self, *args, **kwargs):
        """
        A wrapper of ``tepkit.utils.mpl_tools.ticker_tools.set_axes_ticker_locator()``.

        Set ``ax`` as ``self.ax``.
        """
        set_axes_ticker_locator(self.ax, *args, **kwargs)

    def set_formatter(self, *args, **kwargs):
        """
        A wrapper of ``tepkit.utils.mpl_tools.ticker_tools.set_axes_ticker_formatter()``.

        Set ``ax`` as ``self.ax``.
        """
        set_axes_ticker_formatter(self.ax, *args, **kwargs)

    def save(self, path="tepkit.figure.png", **kwargs) -> None:
        """
        A wrapper of ``matplotlib.figure.Figure.savefig()``.

        Features
        ========
        - Add parameter aliases:
            - ``path``: ``fname``
        - Add parameter default value:
            - ``path``: ``tepkit.figure.png``
        """
        self.fig.savefig(path, **kwargs)

    def show(self, dpi=200):
        """
        A wrapper of ``matplotlib.pyplot.show()``.

        Features
        ========
        - Add new parameters:
            - ``dpi``: Change the dpi of the figure before show it to avoid covering too much of the screen.
        """
        if dpi is not None:
            self.fig.set_dpi(dpi)
        plt.show()


if __name__ == "__main__":
    pass
