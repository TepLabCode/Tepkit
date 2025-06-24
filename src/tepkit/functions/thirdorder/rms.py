from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd

from tepkit.cli import logger
from tepkit.io.shengbte import ForceConstants3rd
from tepkit.io.vasp import Poscar
from tepkit.utils.mpl_tools.plotters.rms_plotter import RmsPlotter
from tepkit.utils.typing_tools import AutoValue


def rms_command(
    work_dir: Path = "./",
    fc_name: str = "FORCE_CONSTANTS_3RD",
    sposcar_name: str = "3RD.SPOSCAR",
    poscar_name: str = "POSCAR",
    save_dir: Path = "./",
    save_name: str = "Auto",
    plot: bool = True,
    nth: bool = True,
    log: bool = True,
    xlim: tuple[float, float] = (AutoValue, AutoValue),
    ylim: tuple[float, float] = (AutoValue, AutoValue),
    distance: str = "d_min",
    fit: bool = False,
) -> None:
    """
    Calculate and Plot the root-mean-square (RMS) of FORCE_CONSTANTS_3RD.

    Required Files:
    | FORCE_CONSTANTS_3RD
    | SPOSCAR
    | POSCAR
    Output Files:
    | tepkit.RMS_of_3rdIFCs.csv
    | tepkit.RMS_of_3rdIFCs.png

    :param work_dir : The directory where the required files is located.
    :param fc_name  : The name of the FORCE_CONSTANTS file.
    :param sposcar_name: The name of the SPOSCAR file.
    :param poscar_name: The name of the unitcell POSCAR file.
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
    :typer poscar       flog: --poscar, --uc
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
        poscar_name=poscar_name,
        save_dir=save_dir,
        save_name=save_name,
        plot=plot,
        nth=nth,
        log=log,
        xlim=xlim,
        ylim=ylim,
        distance=distance,
        fit=fit,
    )


def rms(
    work_dir: Path | str = "./",
    fc_name: str = "FORCE_CONSTANTS_3RD",
    sposcar_name: str = "3RD.SPOSCAR",
    poscar_name: str = "POSCAR",
    save_dir: Path | str | Literal["work_dir"] = "./",
    save_name: str | Literal["Auto"] = "Auto",
    plot: bool = True,
    nth: bool = True,
    log: bool = False,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    distance: Literal["d_ab", "d_ac", "d_bc", "d_min", "d_max", "d_avg"] = "d_min",
    fit: bool = False,
) -> pd.DataFrame:
    """
    Check ``tepkit.functions.thirdorder.rms.rms_command()``
    """

    # Read IFCs
    work_dir: Path = Path(work_dir).resolve()
    logger.step("(1/4) Reading FORCE_CONSTANTS_3RD ...")
    fc = ForceConstants3rd.from_dir(work_dir, file_name=fc_name)

    # Get RMS
    logger.step("(2/4) Calculating RMS ...")
    fc.calculate_rms()
    df = fc.df

    # Get Distances
    logger.step("(3/4) Calculating distances between atoms...")
    poscar = Poscar.from_dir(work_dir, file_name=poscar_name)
    sposcar = Poscar.from_dir(work_dir, file_name=sposcar_name)
    fc.calculate_ion_positions(poscar)
    fc.calculate_ion_distances(sposcar)
    df["distance"] = df[distance]

    # Save Results
    logger.step("(4/4) Saving the results ...")
    logger.info("Saving the data ...")
    # Save Name
    if save_dir == "work_dir":
        save_dir: Path = work_dir
    else:
        save_dir: Path = Path(save_dir).resolve()
    if save_name.lower() == "auto":
        save_name = "tepkit.RMS_of_3rdIFCs"
    csv_path = save_dir / f"{save_name}.csv"
    result_df = df[["rms", "d_ab", "d_ac", "d_bc", "d_min", "d_max", "d_avg"]]
    result_df.to_csv(csv_path, index=False)
    logger.success(f"{save_name}.csv saved to {csv_path}.")
    # Plot
    match distance:
        case "d_min":
            xlabel = "Minimum Distance (Å)"
        case "d_max":
            xlabel = "Maximum Distance (Å)"
        case "d_avg":
            xlabel = "Average Distance (Å)"
        case _:
            xlabel = "Distance (Å)"
    if plot:
        logger.info("Ploting the figure ...")
        RmsPlotter.plot(
            df=df,
            nth=nth,
            sposcar=sposcar,
            log=log,
            xlim=xlim,
            ylim=ylim,
            xlabel=xlabel,
            ylabel="RMS of 3rd IFCs",
            fit=fit,
        )
        if log:
            save_name += "-log"
        fig_path = save_dir / f"{save_name}-{distance}.png"
        plt.savefig(fig_path)
        logger.success(f"{save_name}.png saved to {fig_path}.")

    # End
    logger.success("Finish!")

    # Return
    return result_df
