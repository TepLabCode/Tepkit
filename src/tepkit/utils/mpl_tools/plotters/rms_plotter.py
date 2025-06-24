import numpy as np
from matplotlib import pyplot as plt

from tepkit.cli import logger
from tepkit.io.vasp import Poscar
from tepkit.utils.mpl_tools import Figure, set_axes_ticker_locator


class RmsPlotter:
    @staticmethod
    def plot(
        df,
        nth: bool = False,
        sposcar: Poscar = None,
        log: bool = True,
        xlim: tuple[float, float] | None = None,
        ylim: tuple[float, float] | None = None,
        xlabel: str = "Distance (Å)",
        ylabel: str = "RMS of IFCs",
        fit: bool = False,
    ) -> Figure:
        # Initialization
        figure = Figure(height=0.7, dpi=600, font_size=5)
        fig = figure.fig
        ax = figure.ax
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.subplots_adjust(left=0.18, bottom=0.21, right=0.95, top=0.94)
        ax.xaxis.set_label_coords(0.5, -0.16)
        ax.yaxis.set_label_coords(-0.15, 0.5)

        # Plot Data
        x = df["distance"]
        y = df["rms"]
        plt.scatter(x, y, marker="+", s=12, alpha=1)

        # Adjust Ranges
        if (xlim is not None) and (xlim != (0, 0)):
            plt.xlim(xlim)
        if (ylim is not None) and (ylim != (0, 0)):
            plt.ylim(ylim)

        # Adjust Tickers
        x_range = plt.xlim()[-1] - plt.xlim()[0]
        gap_x = 0.4 if x_range < 5 else max(plt.xlim()[-1] // 7, 1)
        # if x_range < 5, gap_x == 0.4 (0.2)
        # elif 5 <= x_range < 14, gap_x == 1 (0.5)
        # elif 14 <= x_range < 21, gap_x == 2 (1) ...
        set_axes_ticker_locator(ax, "x", "gap", gap_x)
        set_axes_ticker_locator(ax, "x", "gap", gap_x / 2, minor=True)
        if log:
            plt.yscale("log")
            set_axes_ticker_locator(ax, "y", "log", {"subs": (1.0,)})
            set_axes_ticker_locator(ax, "y", "log", {"subs": (0.5,)}, minor=True)
        else:
            y_range = plt.ylim()[-1] - plt.ylim()[0]
            gap_y = max(y_range // 5, 0.2)
            # if y_range < 5, gap_y == 0.2 (0.1)
            # elif 5 <= y_range < 10, gap_y == 1 (0.5)
            # elif 10 <= y_range < 15, gap_y == 2 (1) ...
            set_axes_ticker_locator(ax, "y", "gap", gap_y)
            set_axes_ticker_locator(ax, "y", "gap", gap_y / 2, minor=True)
        ax.tick_params(
            axis="both",
            which="both",
            direction="out",
            top=False,
        )

        # Plot Neighbor Distances
        plt.axvline(
            x=0,
            color="#AAA",
            linestyle="dashdot",
            linewidth=0.5,
        )
        if nth:
            logger.info("Calculating the n-th neighbor distances ...")
            distances = []
            # Fliter out the distances outside the x-axis range
            for i in sposcar.get_neighbor_distances():
                if i < plt.xlim()[-1]:
                    distances.append(i)
            # ┌ calculate the height of the text "n"
            n_text_ys = np.linspace(0.85, 0.4, len(distances))
            x_min, x_max = plt.xlim()
            for n, distance in enumerate(distances, start=0):
                if (distance < x_min) or (distance > x_max):
                    # Ignore the distances outside the x-axis range
                    continue
                if len(distances) > 20 and n > 10 and n % 5 != 0:
                    # If total size of distances is more than 20,
                    # only show distances like (1, 2, ..., 9, 10, 15, 20, ...)
                    continue
                plt.axvline(
                    x=distance,
                    color="grey",
                    linestyle="--",
                    label="nth",
                    linewidth=0.5,
                )
                plt.text(
                    x=(distance - x_min) / (x_max - x_min) + 0.01,
                    y=float(n_text_ys[n]),
                    s=str(n),
                    fontsize=8,
                    ha="left",
                    va="center",
                    color="grey",
                    transform=ax.transAxes,
                )

        # Fitting
        if fit:
            log_y = [np.log(i) for i in y.values if i > 0]

            slope, intercept = np.polyfit(x, log_y, 1)
            x_lim = ax.get_xlim()
            x_fit = np.linspace(0, x_lim[1], 100)
            y_fit = np.exp(slope * x_fit + intercept)
            plt.plot(x_fit, y_fit, color="orange", linestyle=(0, (6.4, 1.6)))
            ax.set_xlim(x_lim)
            text = plt.text(
                x=0.02,
                y=0.03,
                s=f"$\ln y = {slope:.2f} \cdot x + {intercept:.2f}$",
                fontsize=6,
                ha="left",
                va="bottom",
                color="black",
                transform=fig.transFigure,
                bbox=dict(
                    boxstyle="round,pad=0.4",
                    edgecolor="orange",
                    facecolor="white",
                    linewidth=0.6,
                ),
            )
            logger.info(f"Fitting Function: y = exp({slope:.4f} * x + {intercept:.4f})")

        # Return
        return figure
