from tepkit.core.symmetry import Axis, LayerGroup, BravaisLattice2D
from tepkit.utils.rich_tools import print_table


def get_layer_group(
    path,
    fmt: str = "POSCAR",
    aperiodic_axis: str = "a3",
    sym_prec: float = 1e-5,
    detail: bool = False,
):
    """
    Get the layer group of a 2D structure.

    :param fmt: Only support POSCAR now.
    :param aperiodic_axis: (a1 / a2 / a3) Only a3 is tested.
    :param sym_prec: The precision of symmetry detection.
    :param detail: Print all data about the layer group.

    :typer aperiodic_axis flag: --aperiodic-axis, --axis
    :typer sym_prec flag: -p, --prec
    :typer detail flag: -d, --detail
    """
    layer_group = LayerGroup.from_file(
        path,
        fmt=fmt,
        aperiodic_axis=Axis[aperiodic_axis],
        sym_prec=sym_prec,
    )
    bravais_lattice_2d = BravaisLattice2D.from_file(
        path,
        fmt=fmt,
        sym_prec=sym_prec,
    )
    detail_data = layer_group.data

    sg_title = "===== Space-group Information ====="
    sg_data = {
        "Space Group (No.)": detail_data.pop("sg_number"),
        "Space Group (Symbol)": detail_data.pop("sg_international"),
    }
    print_table(
        dictionary=sg_data,
        title=sg_title,
        key="",
        value="",
        table_options={
            "show_header": False,
            "show_lines": True,
            "title_justify": "left",
            "min_width": len(sg_title),
        },
        key_options={"justify": "right"},
    )
    lg_title = "===== Layer-group Information ====="
    important_data = {
        "Layer Group (No.)": detail_data.pop("number"),
        "Layer Group (Symbol)": detail_data.pop("international"),
        "Point Group": detail_data.pop("pointgroup"),
        "Bravais Lattice (2D)": bravais_lattice_2d.to_string(style="full"),
        "Bravais System (2D)": detail_data.pop("bravais_system_2d"),
        "Crystal System (3D)": detail_data.pop("crystal_system_3d"),
    }
    print_table(
        dictionary=important_data,
        title=lg_title,
        key="",
        value="",
        table_options={
            "show_header": False,
            "show_lines": True,
            "title_justify": "left",
            "min_width": len(lg_title),
        },
        key_options={"justify": "right"},
    )
    if detail:
        # Suppress small values
        import numpy as np

        for key in ["origin_shift", "translations", "std_lattice"]:
            detail_data[key] = np.array2string(detail_data[key], suppress_small=True)

        # Print
        print_table(
            dictionary=detail_data,
            title="===== Details =====",
            table_options={
                "show_header": False,
                "show_lines": True,
                "title_justify": "left",
            },
            key_options={"justify": "right"},
        )
