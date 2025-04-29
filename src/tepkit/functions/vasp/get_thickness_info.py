from pathlib import Path

from loguru import logger
from tepkit.io.vasp import Poscar
from tepkit.utils.rich_tools import print_table
import toml


def get_thickness_info(
    poscar: Path = "./POSCAR",
    save: bool = True,
    to_path: str = "./tepkit.thickness_info.toml",
):
    """
    Get the structure thickness information of POSCAR.

    :param poscar : The path of POSCAR.
    :param save   : Whether to save information to save_path.
    :param to_path: The file path to save information.

    :typer poscar  flag: --poscar, -p
    :typer save    flag: --save, -s
    :typer to_path flag: --to, -t
    """
    # Read
    logger.info(f'Reading file "{poscar}" ...')
    poscar = Poscar.from_file(poscar)
    info_dict = poscar.thickness_info

    # Print
    print_table(
        info_dict,
        title="Thickness Information",
        key="Quantities",
        value="Values",
    )

    # Save
    if save:
        logger.info(f'Saving thickness information to "{to_path}".')
        with open(to_path, "w") as file:
            toml.dump(info_dict, file)

    # End
    logger.success(f"Finish!")
