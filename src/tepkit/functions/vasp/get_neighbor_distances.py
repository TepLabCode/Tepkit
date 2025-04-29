from tepkit.utils.rich_tools import print_table
from tepkit.io.vasp import Poscar
from loguru import logger
from pathlib import Path


def get_neighbor_distances(
    poscar: Path = "./POSCAR",
    decimal: int = 4,
    max_nth: int = 30,
):
    """
    Get the distances of atoms to its n-th neighborn.

    :param poscar : The path of POSCAR file.
    :param decimal: Decimal places of distances.
    :param max_nth: The maximum of n-th neighbors to be calculated. &
                    [bright_black](will affect the calculation time)[/bright_black]

    :typer poscar  flag: --poscar, -p
    :typer decimal flag: --decimal, -d
    :typer max_nth flag: --max-n, -m
    """
    poscar = Poscar.from_file(poscar)
    logger.info("Calculating distances for each atom ...")
    distances = poscar.get_neighbor_distances(max_nth=max_nth)
    infos = {i: f"{distances[i]:.{decimal}f}" for i in range(len(distances))}
    logger.opt(colors=True).success("<g>Done.</>")
    logger.info("The distances are:")
    print_table(
        infos,
        key="Neighborn\n(n-th)",
        value="Distance\n(Angstrom)",
        table_options={"box": None},
        key_options={"justify": "center"},
        value_options={"justify": "right"},
    )
    if len(distances) == max_nth + 1:
        logger.log(
            "NOTE", "Reached max-nth, you can increase max-nth to get more results."
        )
