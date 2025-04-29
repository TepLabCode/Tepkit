from enum import Enum
from pathlib import Path

from loguru import logger
from pandas import DataFrame

from tepkit.io.output import save_df
from tepkit.io.vasp import Eigenval
from tepkit.io.vasp.outcar import Outcar


class KpointsChoices(str, Enum):
    all_points = "all"
    weighted = "w"
    zero_weighted = "zw"


def get_band(
    eigenval: Path = "./EIGENVAL",
    index: str = "all",
    kpoints: KpointsChoices = KpointsChoices.all_points.value,
    ref: str = 0.0,
    output: str = "auto",
    fmt: str = "auto",
    distance: bool = False,
    poscar: Path = "./POSCAR",
    outcar: Path = "./OUTCAR",
    soc: bool = None,
) -> DataFrame:
    R"""
    Get the data of the electronic band structure to a table file.

    - All options is optional, the simplest usage is just run
      `tepkit vasp f03` in your vasp work dir.
    - If you want to get data to plot electronic band structure on path,
      └ use: `--kpoints zw` and `--distance`.

    :param eigenval: The path of EIGENVAL file.
    :param index   : Select the needed band index. &
                     [green]( all / VBE / CBE / \[int] )[/green]
    :param kpoints : Select the needed k-points. &
                     [green]( all / w: weighted / zw: zero-weighted )[/green]
    :param ref     : Select the reference level of energy. &
                     [green]( outcar_fermi / midgap / \[float (eV)] )[/green]
    :param output  : The path to save the output file.
    :param fmt     : The format of the output file. &
                     [green]( csv / xlsx(excel) / pickle )[/green]
    :param distance: Get the distance in the reciprocal space
                     between each k-point and its previous one
                     cumulatively.
    :param poscar  : The path of POSCAR file. &
                     ( Only used when --distance )
    :param outcar  : The path of OUTCAR file. &
                     ( Only used when --ref is `outcar_fermi` )
    :param soc     : Whether the SOC is used in the calculation. &
                     ( Only used when --index is `VBE` or `CBE` )

    :typer index   metavar: TEXT|INT
    :typer kpoints metavar: TEXT
    :typer fmt     metavar: TEXT
    :typer ref     metavar: TEXT|FLOAT
    :typer output  metavar: PATH

    :typer eigenval flag: --eigenval, -e
    :typer kpoints  flag: --kpoints, -k
    :typer output   flag: --output, -o
    :typer distance flag: --distance, -d
    :typer fmt      flag: --format, -f
    :typer soc      flag: --soc

    :typer poscar panel: Conditional Options
    :typer outcar panel: Conditional Options
    :typer soc    panel: Conditional Options

    :typer eigenval exists: True
    """
    # process `eigenval`
    eig_path = Path(eigenval)
    eig = Eigenval.from_file(eig_path)
    # process `soc`
    eig.soc = soc
    # process `index`
    if index.lower() != "all":
        df = eig.get_band(index=index)
    else:
        df = eig.df
    # process `kpoints`
    match kpoints:
        case KpointsChoices.all_points:
            pass
        case KpointsChoices.weighted:
            df = df[df.fermi_weight != 0]
        case KpointsChoices.zero_weighted:
            df = df[df.fermi_weight == 0]
        case _:
            raise ValueError
    # process `ref`
    match ref.lower():
        case "outcar_fermi":
            outcar = Outcar.from_file(outcar)
            ref_e = outcar.fermi_energy
        case "midgap":
            ref_e = eig.energy_midgap
        case _:
            ref_e = float(ref)
    df["energy-ref"] = df["energy"] - ref_e
    # when used as python function
    if output is None:
        return df
    # auto_name
    auto_name = "-".join(
        [
            eig_path.name,
            f"i{index.upper()}",
            f"k{kpoints.upper()}",
            f"r{ref.upper()}",
        ]
    )
    auto_name += ".csv"
    # Save
    save_path = auto_name if output == "auto" else output
    save_df(df, to_path=save_path, fmt=fmt)
    logger.opt(colors=True).success(
        f"Data table has been saved to <blue>{save_path}</blue>."
    )
    return df
