from pathlib import Path

import numpy as np
from mendeleev import element
from tqdm import tqdm

from tepkit.cli import logger
from tepkit.functions.phonopy.rms import rms
from tepkit.io.vasp import Poscar
from tepkit.utils.colors import tepkit_colors
from tepkit.utils.mpl_tools import Figure


def main(
    work_dir: Path | str,
    line_color: str = "red",
    ion_scales: list[float] = None,
    ion_colors: list[str] | None = None,
    at_least: int | float = 0,
):
    df = rms(
        work_dir=work_dir,
        plot=False,
    )
    sposcar = Poscar.from_dir(work_dir, file_name="SPOSCAR")
    positions = sposcar.get_cartesian_ion_positions()

    # Create a 3D plot
    figure = Figure(projection="3d")
    ax = figure.ax

    # Each line represents an IFC
    logger.info("Plotting lines ...")
    for index, row in tqdm(list(df.iterrows())):
        rms_value = row["rms"]
        # Skip small RMS values
        if rms_value < at_least:
            continue
        d = row["distance"]
        # Get ion indexes
        ion_a = int(row["atom_a"])
        ion_b = int(row["atom_b"])
        # Get ion positions
        xyz_a = positions[ion_a - 1]
        xyz_b = positions[ion_b - 1]
        # Calculate distance between ions
        distance = np.linalg.norm(xyz_a - xyz_b)
        # Skip ion pairs outside the unit cell
        if abs(distance - d) > 1e-5:
            continue
        # Build line coordinates
        x_values = [xyz_a[0], xyz_b[0]]
        y_values = [xyz_a[1], xyz_b[1]]
        z_values = [xyz_a[2], xyz_b[2]]
        # Plot lines
        ax.plot(
            x_values,
            y_values,
            z_values,
            color=line_color,
            linewidth=rms_value * 2,
            alpha=min(rms_value * 0.2, 1),
        )
    # Plot ions
    species_indexes = sposcar.species_index_per_ion
    species_names = sposcar.species_name_per_ion
    ion_colors = ion_colors or list(tepkit_colors.values())
    if not ion_scales:
        ion_scales = [1.0] * len(sposcar.species_names)
    vdw_radius_dict = {
        species_name: element(species_name).vdw_radius / 100
        for species_name in sposcar.species_names
    }
    logger.info("Plotting ions ...")
    for i, xyz in enumerate(positions):
        type_index = species_indexes[i]
        color = ion_colors[type_index]
        ion_scale = ion_scales[type_index]
        vdw_radius = vdw_radius_dict[species_names[i]]
        ax.plot(
            xyz[0],
            xyz[1],
            xyz[2],
            "o",
            color=color,
            ms=vdw_radius * 2 * ion_scale,
            markeredgecolor="black",
            markeredgewidth=0.5,
            zorder=xyz[2],
        )
    # Adjust plot
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    figure.set_locator("x", "gap", 5)
    figure.set_locator("y", "gap", 5)
    figure.set_locator("z", "gap", 5)
    ax.set_proj_type("ortho")
    ax.set_aspect("equal")
    return figure


if __name__ == "__main__":
    _figure = main(
        work_dir=Path("./input"),
        ion_scales=[1.0, 0.9],
        ion_colors=["#C13BE0", "orange"],
    )
    # _figure.show()
    _fig = _figure.fig
    _ax = _figure.ax
    _ax.set_xlim(-10, 17)
    _ax.set_ylim(-2, 17)
    _ax.set_zlim(8, 22)
    _ax.set_aspect("equal")
    # oblique view
    logger.info("Saving the figures ...")
    logger.step("1/4 ...")
    _ax.view_init(elev=20, azim=-60)
    _figure.save("tepkit.RMS_of_2ndIFCs.png")
    # Side view
    logger.step("2/4 ...")
    _figure.adjust_margin(left=200, right=20, bottom=20, top=20)
    _ax.view_init(elev=0, azim=0)
    _figure.save("tepkit.RMS_of_2ndIFCs-a.png")
    # Front view
    logger.step("3/4 ...")
    _ax.view_init(elev=0, azim=-90)
    _figure.save("tepkit.RMS_of_2ndIFCs-b.png")
    # Top view
    logger.step("4/4 ...")
    _ax.view_init(elev=90, azim=-90)
    _figure.save("tepkit.RMS_of_2ndIFCs-c.png")
    logger.success("Finish!")
