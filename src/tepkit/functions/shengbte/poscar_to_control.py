from tepkit.cli import logger
from tepkit.io.shengbte import Control
from tepkit.utils.rich_tools import print_panel


def poscar_to_control(
    poscar: str = "./POSCAR",
    temperature: int = None,
    temperatures: tuple[int, int, int] = (None, None, None),
    ngrid: tuple[int, int, int] = (1, 1, 1),
    supercell: tuple[int, int, int] = (1, 1, 1),
    path: str = "./CONTROL",
):
    """
    generate the CONTROL file from POSCAR file.

    :param poscar      : Path of POSCAR file
    :param temperature : Single value of temperature (priority)
    :param temperatures: [T_min, T_max(include), T_step]
    :param ngrid       : Value of ngrid
    :param supercell   : Supercell of FORCE_CONSTANTS_2ND
    :param path        : Save path of CONTROL file

    :typer poscar       flag: --poscar, -p
    :typer temperature  flag: --temperature, -t
    :typer temperatures flag: --temperatures, --ts
    :typer ngrid        flag: --ngrid, -n
    :typer supercell    flag: --supercell, --sc
    :typer path         flag: --path

    :typer poscar       metavar: PATH
    :typer temperatures metavar: [INT INT INT]
    :typer ngrid        metavar: [INT INT INT]
    :typer supercell    metavar: [INT INT INT]
    :typer path         metavar: PATH
    """
    control = Control.from_poscar(poscar)
    if temperature is not None:
        control.temperature = temperature
    elif temperatures != (None, None, None):
        control.temperatures = temperatures
    else:
        control.temperature = 300
    control.ngrid = ngrid
    control.scell = supercell
    logger.info("The CONTROL file will be generated as below:")
    print_panel(str(control), title=path, expand=False)
    control.write(path=path)
    logger.success(f"The CONTROL file is saved to {path}.")
