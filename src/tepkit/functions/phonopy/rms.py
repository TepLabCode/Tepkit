from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd

from tepkit.cli import logger
from tepkit.io.phonopy import ForceConstants
from tepkit.io.vasp import Poscar
from tepkit.utils.mpl_tools.plotters.rms_plotter import RmsPlotter
from tepkit.utils.typing_tools import AutoValue


def rms_command(
    work_dir: Path = "./",
    fc_name: str = "FORCE_CONSTANTS",
    sposcar_name: str = "SPOSCAR",
    save_dir: Path = "./",
    save_name: str = "Auto",
    plot: bool = True,
    nth: bool = True,
    log: bool = False,
    xlim: tuple[float, float] = (AutoValue, AutoValue),
    ylim: tuple[float, float] = (AutoValue, AutoValue),
    fit: bool = False,
) -> None:
    """
    Calculate and Plot the root-mean-square (RMS) of FORCE_CONSTANTS (FORCE_CONSTANTS_2ND).

    Required Files:
    | FORCE_CONSTANTS
    | SPOSCAR
    Output Files:
    | tepkit.RMS_of_2ndIFCs.csv
    | tepkit.RMS_of_2ndIFCs.png

    :param work_dir : The directory where the required files is located.
    :param fc_name  : The name of the FORCE_CONSTANTS file.
    :param sposcar_name: The name of the SPOSCAR file.
    :param save_dir : The directory where the output files will be saved. &
                      (`--save-dir work_dir` will save the files to `work_dir`)
    :param save_name: The name of the output files.
    :param plot     : Whether to plot the figure of data.
    :param nth      : Show the distances of the atoms' n-th neighbor.
    :param xlim     : The range of the x-axis.
    :param ylim     : The range of the y-axis.
    :param log      : Set the y-axis to logarithmic coordinates.

    :typer work_dir     flag: --work-dir, -d
    :typer fc_name      flag: --fc
    :typer sposcar_name flag: --sposcar, --sc
    :typer save_name    flag: --save-name, -s
    :typer log          flag: --log/--linear

    :typer xlim metavar: MIN MAX
    :typer ylim metavar: MIN MAX

    :typer plot panel: Plot Settings
    :typer nth  panel: Plot Settings
    :typer xlim panel: Plot Settings
    :typer ylim panel: Plot Settings
    :typer log  panel: Plot Settings
    """
    rms(
        work_dir=work_dir,
        fc_name=fc_name,
        sposcar_name=sposcar_name,
        save_dir=save_dir,
        save_name=save_name,
        plot=plot,
        nth=nth,
        log=log,
        xlim=xlim,
        ylim=ylim,
        fit=fit,
    )


def rms(
    work_dir: Path | str = "./",
    fc_name: str = "FORCE_CONSTANTS",
    sposcar_name: str = "SPOSCAR",
    save_dir: Path | str | Literal["work_dir"] = "./",
    save_name: str | Literal["Auto"] = "Auto",
    plot: bool = True,
    nth: bool = True,
    log: bool = False,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    fit: bool = False,
) -> pd.DataFrame:
    """
    Check ``tepkit.functions.phonopy.rms.rms_command()``
    """

    # Read IFCs
    work_dir: Path = Path(work_dir).resolve()
    logger.step("(1/4) Reading FORCE_CONSTANTS ...")
    fc = ForceConstants.from_dir(work_dir, file_name=fc_name)

    # Get RMS
    logger.step("(2/4) Calculating RMS ...")
    fc.calculate_rms()
    df = fc.df

    # Get Distances
    logger.step("(3/4) Calculating distances between atoms...")
    sposcar = Poscar.from_dir(work_dir, file_name=sposcar_name)
    distances = sposcar.get_interatomic_distances()
    df["distance"] = df.apply(
        lambda row: distances[row["atom_a"] - 1][row["atom_b"] - 1], axis=1
    )

    # Save Results
    logger.step("(4/4) Saving the results ...")
    logger.info("Saving the data ...")
    # Save Name
    if save_dir == "work_dir":
        save_dir: Path = work_dir
    else:
        save_dir: Path = Path(save_dir).resolve()
    if save_name.lower() == "auto":
        save_name = "tepkit.RMS_of_2ndIFCs"
    csv_path = save_dir / f"{save_name}.csv"
    result_df = df[["rms", "distance", "atom_a", "atom_b"]]
    result_df.to_csv(csv_path, index=False)
    logger.success(f"{save_name}.csv saved to {csv_path}.")
    # Plot
    if plot:
        logger.info("Ploting the figure ...")
        RmsPlotter.plot(
            df=df,
            nth=nth,
            sposcar=sposcar,
            log=log,
            xlim=xlim,
            ylim=ylim,
            ylabel="RMS of 2nd IFCs",
            fit=fit,
        )
        if log:
            save_name += "-log"
        fig_path = save_dir / f"{save_name}.png"
        plt.savefig(fig_path)
        logger.success(f"{save_name}.png saved to {fig_path}.")

    # End
    logger.success("Finish!")

    # Return
    return result_df
