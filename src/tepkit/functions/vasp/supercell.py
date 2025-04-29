from pathlib import Path
from tepkit.io.vasp import Poscar
from loguru import logger


def supercell(
    na: int,
    nb: int,
    nc: int,
    poscar: Path = "./POSCAR",
    output: Path = "Auto",
) -> None:
    """
    Generate the supercell of POSCAR.

    :param na    : The multiples of the supercell along the a-axis.
    :param nb    : The multiples of the supercell along the b-axis.
    :param nc    : The multiples of the supercell along the c-axis.
    :param poscar: The path of POSCAR file.
    :param output: The path to save the output file.

    :typer na argument:
    :typer nb argument:
    :typer nc argument:
    :typer poscar exists: True
    """
    unitcell = Poscar.from_file(poscar)
    sc = unitcell.to_supercell(na, nb, nc)
    if output == Path("Auto"):
        filename = poscar.stem
        if filename.endswith(".poscar"):
            filename = filename[:-7]
        output = f"{filename}.sc{na}{nb}{nc}.poscar.vasp"
    sc.to_file(output)
    logger.opt(colors=True).success(
        f"The <lc>{na} x {nb} x {nc}</> supercell of <e>{poscar}</> was saved to <e>{output}</>."
    )
