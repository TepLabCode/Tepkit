from pathlib import Path

from tepkit.cli import logger
from tepkit.io.vasp import ExplicitKpoints, Kpoints, Poscar
from tepkit.utils.mpl_tools import Figure
from tepkit.utils.typing_tools import PathLike


def _plot_kpoints(
    kpoints: ExplicitKpoints,

    save_path: PathLike,
    axis: bool = True,
):
    """
    TODO：UnderTest
    """
    figure = Figure(
        height=1,
        # style="default",
        dpi=300,
    )
    figure.adjust_margin(
        left=170,
        right=40,
        bottom=120,
        top=40,
    )
    ax = figure.ax
    if axis:
        ax.axis("on")
        ax.tick_params(direction="out")
        ax.tick_params(top=False, right=False)
        # ax.set_xlabel("$k_x$")
        # ax.set_ylabel("$k_y$")
        figure.adjust_margin(
            left=170,
            right=40,
            bottom=100,
            top=40,
        )
    else:
        ax.axis("off")
        figure.adjust_margin(
            left=40,
            right=40,
            bottom=40,
            top=40,
        )
    kpoints.plot(ax=ax, save_path=save_path)
    logger.c.success(f"The visualization image has been saved to <cyan>{save_path}</>.")


def get_bz_kpoints(
    poscar: str = "./POSCAR",
    density: int = 10,
    edge_density: int = 15,
    save_path: str = "KPOINTS",
    preview: bool = False,
    mode: str = "half",
):
    """
    Generate the KPOINTS file covering the 2D Brillouin zone.

    :typer poscar flag: --poscar, -p
    :typer density flag: --density, -d
    :typer edge_density flag: --edge-density, -e
    :typer save_path flag: --save-path, -s
    :typer preview flag: --preview, -v
    :typer mode flag: --mode, -m
    """
    poscar = Poscar.from_file(poscar)
    kpoints = Kpoints.get_2d_bz_kpoints(
        b_lattice=poscar.get_reciprocal_lattice(with_2pi=False),
        density=density,
        edge_density=edge_density,
        mode=mode,
    )
    kpoints.to_file(save_path)
    logger.c.info(
        f"KPOINTS file with {kpoints.num_kpts} k-points has been saved to <cyan>{save_path}</>."
    )
    if preview:
        _plot_kpoints(kpoints, save_path=f"{save_path}.png")


def plot_ibzkpt(
    path: str = "Auto",
    poscar: Path = "./POSCAR",
    save_path: str = "Auto ({file_name}.png)",
    axis: bool = True,
):
    """
    Plot the visualization image of IBZKPT or Explicit-mode KPOINTS file.

    :param path: The path of IBZKPT or KPOINTS file.
    :param poscar: The path of POSCAR file.
    :param save_path: The path to save the image.

    :typer path argument:
    :typer poscar flag: --poscar
    :typer save_path flag: --to
    """
    if path == "Auto":
        if Path("IBZKPT").exists():
            path = Path("IBZKPT")
        elif Path("KPOINTS").exists():
            path = Path("KPOINTS")
        else:
            raise FileNotFoundError("No IBZKPT or KPOINTS file found.")
    else:
        path = Path(path)
    logger.c.step(f"Reading <i>k</>-points from <cyan>{path}</>.")
    kpoints = ExplicitKpoints.from_file(path)
    logger.c.step(f"Reading lattice from <cyan>{poscar}</>.")
    poscar = Poscar.from_file(poscar)
    kpoints.b_lattice = poscar.get_reciprocal_lattice(with_2pi=False)
    if save_path == "Auto ({file_name}.png)":
        save_path = Path(f"./{path.stem}.png")
    logger.c.step(f"Ploting...")
    _plot_kpoints(kpoints, save_path, axis=axis)
