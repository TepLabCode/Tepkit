from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from tepkit.cli import logger
from tepkit.io.indices import T3D_INDICES
from tepkit.io.phonopy import ForceConstants
from tepkit.io.vasp import Poscar
from tepkit.utils.mpl_tools import Figure
from tepkit.utils.mpl_tools.ticker_tools import set_axes_ticker_locator
from tepkit.utils.typing_tools import AutoValue


def plot_rms(
    df,
    nth: bool = False,
    sposcar: Poscar = None,
    log: bool = True,
    xlim: tuple[float, float] = None,
    ylim: tuple[float, float] = None,
) -> Figure:
    # Initialization
    figure = Figure(height=0.7, dpi=600, font_size=5)
    ax = figure.ax
    plt.xlabel("Distance (Å)")
    plt.ylabel("RMS of 2nd IFCs")
    plt.subplots_adjust(left=0.18, bottom=0.21, right=0.95, top=0.94)
    ax.xaxis.set_label_coords(0.5, -0.16)
    ax.yaxis.set_label_coords(-0.15, 0.5)

    # Plot Data
    x = df["distance"]
    y = df["rms"]
    plt.scatter(x, y, marker="+", s=12, alpha=1)

    # Adjust Ranges
    if xlim != (0, 0):
        plt.xlim(xlim)
    if ylim != (0, 0):
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

    # Return
    return figure


def rms(
    work_dir: Path = "./",
    save_dir: Path = "./",
    save_name: str = "Auto",
    plot: bool = True,
    nth: bool = True,
    log: bool = False,
    xlim: tuple[float, float] = (AutoValue, AutoValue),
    ylim: tuple[float, float] = (AutoValue, AutoValue),
):
    """
    Calculate and Plot the root-mean-square (RMS) of FORCE_CONSTANTS.

    Required Files:
    | FORCE_CONSTANTS
    | SPOSCAR
    Output Files:
    | tepkit.RMS_of_2ndIFCs.csv
    | tepkit.RMS_of_2ndIFCs.png

    :param work_dir : The directory where the required files is located.
    :param save_dir : The directory where the output files will be saved. &
                      (`--save-dir work_dir` will save the files to `work_dir`)
    :param save_name: The name of the output files.
    :param plot     : Whether to plot the figure of data.
    :param nth      : Show the distances of the atoms' n-th neighbor.
    :param xlim     : The range of the x-axis.
    :param ylim     : The range of the y-axis.
    :param log      : Set the y-axis to logarithmic coordinates.

    :typer work_dir  flag: --work-dir, -d
    :typer save_name flag: --save-name, -s
    :typer log      flag: --log/--linear

    :typer xlim metavar: MIN MAX
    :typer ylim metavar: MIN MAX

    :typer plot panel: Plot Settings
    :typer nth  panel: Plot Settings
    :typer xlim panel: Plot Settings
    :typer ylim panel: Plot Settings
    :typer log  panel: Plot Settings
    """
    # Read IFCs
    work_dir = Path(work_dir).resolve()
    logger.step("(1/4) Reading FORCE_CONSTANTS ...")
    fc = ForceConstants.from_dir(work_dir)
    df = fc.df

    # Get RMS
    logger.step("(2/4) Calculating RMS ...")
    df["rms"] = (df[T3D_INDICES].apply(lambda row: row.pow(2)).sum(axis=1) / 9) ** 0.5

    # Get Distances
    logger.step("(3/4) Calculating distances between atoms...")
    sposcar = Poscar.from_dir(work_dir, file_name="SPOSCAR")
    distances = sposcar.get_interatomic_distances()
    df["distance"] = df.apply(
        lambda row: distances[row["atom_a"] - 1][row["atom_b"] - 1], axis=1
    )

    # Save Results
    logger.step("(4/4) Saving the results ...")
    logger.info("Saving the data ...")
    # Save Name
    if save_dir == "work_dir":
        save_dir = work_dir
    if save_name.lower() == "auto":
        save_name = "tepkit.RMS_of_2ndIFCs"
        if log:
            save_name += "-log"
    df[["distance", "rms", "atom_a", "atom_b"]].to_csv(
        save_dir / f"{save_name}.csv", index=False
    )
    logger.success(f"{save_name}.csv saved to {work_dir}.")

    # Plot
    if plot:
        logger.info("Ploting the figure ...")
        plot_rms(
            df=df,
            nth=nth,
            sposcar=sposcar,
            log=log,
            xlim=xlim,
            ylim=ylim,
        )
        plt.savefig(save_dir / f"{save_name}.png")
        logger.success(f"{save_name}.png saved to {work_dir}.")

    # End
    logger.success("Finish!")

    # Return
    return df[["distance", "rms", "atom_a", "atom_b"]]
