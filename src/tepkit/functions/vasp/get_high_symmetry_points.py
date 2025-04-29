from pathlib import Path

import pandas as pd
from tepkit.cli import logger
from tepkit.core.high_symmetry_points import HighSymmetryPoints2D
from tepkit.core.symmetry import BravaisLattice2D

from tepkit.io.output import save_df
from tepkit.io.vasp import Poscar


def get_high_symmetry_points_2d(
    poscar: Path = "./POSCAR",
    save: bool = False,
    to_path: str = "./tepkit.high_symmetry_points_2d.csv",
    fmt: str = "auto",
    border: bool = False,
    decimal: int = 5,
    with_2pi: bool = True,
):
    """
    Get high-symmetry k-points of 2D materials.

    :param poscar : The path of POSCAR.
    :param save   : Whether to save information to save_path.
    :param to_path: The file path to save information.
    :param fmt    :
    :param decimal:
    :param border:
    :param with_2pi: VASP Cartesian KPOINTS use --no-2pi

    :typer poscar  flag: --poscar, -p
    :typer save    flag: --save, -s
    :typer to_path flag: --to, -t
    :typer with_2pi flag: --2pi/--no-2pi

    :typer poscar exists: True
    """
    # Read
    logger.step(f'Reading file "{poscar}" ...')
    poscar = Poscar.from_file(poscar)
    # df = poscar.get_high_symmetry_points_2d(decimal=decimal, with_2pi=with_2pi)
    hsps = HighSymmetryPoints2D.from_poscar(poscar, with_2pi=with_2pi)
    if border:
        edge_type = BravaisLattice2D.from_poscar(poscar).to_string("full")
        logger.opt(colors=True).info(
            f"The border type is recognized as: <lc>{edge_type}</>."
        )
        df = hsps.get_edge_df()
    else:
        df = hsps.df
    out_df = pd.DataFrame()
    out_df[["k_a", "k_b", "k_c"]] = pd.DataFrame(df["k_abc"].tolist(), index=df.index)
    out_df[["k_x", "k_y", "k_z"]] = pd.DataFrame(df["k_xyz"].tolist(), index=df.index)
    pd.options.display.float_format = ("{:.%df}" % decimal).format
    logger.step(f"Showing high symmetry points:")
    print(out_df)

    # Save
    if save:
        save_df(out_df, to_path=to_path, fmt=fmt)
        logger.opt(colors=True).info(
            f"Saving high symmetry points to <lc>{to_path}</>."
        )

    # End
    logger.done(f"Finish!")
