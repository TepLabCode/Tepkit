from pathlib import Path

from tepkit.cli import logger
from tepkit.io.vasp import Poscar

VASP_RECOMMENDED_POTENTIALS_PAW_PBE_64 = {
    # 1
    "H": "H",
    "He": "He",
    # 2
    "Li": "Li_sv",
    "Be": "Be",
    "B": "B",
    "C": "C",
    "N": "N",
    "O": "O",
    "F": "F",
    "Ne": "Ne",
    # 3
    "Na": "Na_pv",
    "Mg": "Mg",
    "Al": "Al",
    "Si": "Si",
    "P": "P",
    "S": "S",
    "Cl": "Cl",
    "Ar": "Ar",
    # 4
    "K": "K_sv",
    "Ca": "Ca_sv",
    "Sc": "Sc_sv",
    "Ti": "Ti_sv",
    "V": "V_sv",
    "Cr": "Cr_pv",
    "Mn": "Mn_pv",
    "Fe": "Fe",
    "Co": "Co",
    "Ni": "Ni",
    "Cu": "Cu",
    "Zn": "Zn",
    "Ga": "Ga_d",
    "Ge": "Ge_d",
    "As": "As",
    "Se": "Se",
    "Br": "Br",
    "Kr": "Kr",
    # 5
    "Rb": "Rb_sv",
    "Sr": "Sr_sv",
    "Y": "Y_sv",
    "Zr": "Zr_sv",
    "Nb": "Nb_sv",
    "Mo": "Mo_sv",
    "Tc": "Tc_pv",
    "Ru": "Ru_pv",
    "Rh": "Rh_pv",
    "Pd": "Pd",
    "Ag": "Ag",
    "Cd": "Cd",
    "In": "In_d",
    "Sn": "Sn_d",
    "Sb": "Sb",
    "Te": "Te",
    "I": "I",
    "Xe": "Xe",
    # 6
    "Cs": "Cs_sv",
    "Ba": "Ba_sv",
    "La": "La",
    "Ce": "Ce",
    "Pr": "Pr_3",
    "Nd": "Nd_3",
    "Pm": "Pm_3",
    "Sm": "Sm_3",
    "Eu": "Eu_2",
    "Gd": "Gd_3",
    "Tb": "Tb_3",
    "Dy": "Dy_3",
    "Ho": "Ho_3",
    "Er": "Er_3",
    "Tm": "Tm_3",
    "Yb": "Yb_2",
    "Lu": "Lu_3",
    "Hf": "Hf_pv",
    "Ta": "Ta_pv",
    "W": "W_sv",
    "Re": "Re",
    "Os": "Os",
    "Ir": "Ir",
    "Pt": "Pt",
    "Au": "Au",
    "Hg": "Hg",
    "Tl": "Tl_d",
    "Pb": "Pb_d",
    "Bi": "Bi_d",
    "Po": "Po_d",
    "At": "At",
    "Rn": "Rn",
    # 7
    "Fr": "Fr_sv",
    "Ra": "Ra_sv",
    "Ac": "Ac",
    "Th": "Th",
    "Pa": "Pa",
    "U": "U",
    "Np": "Np",
    "Pu": "Pu",
    "Am": "Am",
    "Cm": "Cm",
}
"""
Refs:
- [Available pseudopotentials - VASP Wiki](https://www.vasp.at/wiki/Available_pseudopotentials)
- [Choosing pseudopotentials - VASP Wiki](https://www.vasp.at/wiki/Choosing_pseudopotentials)
"""


def write_potcar_from_poscar(
    poscar_path="POSCAR",
    *,
    potcar_path="POTCAR",
    print_info: bool = True,
):
    from pymatgen.io.vasp import Potcar

    logger.step(f"Reading symbols from `{Path(poscar_path).resolve()}`...")
    poscar = Poscar.from_file(poscar_path)
    species_names = poscar.species_names
    logger.info(f"Symbols: {species_names}")

    logger.step(f"Finding recommended potentials...")
    poscar_dict = VASP_RECOMMENDED_POTENTIALS_PAW_PBE_64
    pot_symbols = [poscar_dict[s] for s in species_names]
    logger.info(f"Potentials: {pot_symbols}")

    logger.step(f"Writing {potcar_path} to `{Path(potcar_path).resolve()}`...")
    potcar = Potcar(
        symbols=pot_symbols,
        functional="PBE_64",
    )
    potcar.write_file(potcar_path)
    logger.done(f"Done.")

    if print_info:
        import os
        from parsevasp.potcar import Potcar as PVPotcar
        from rich.console import Console
        from rich.table import Table

        data = {}
        for s in species_names:
            potcar = Potcar(
                symbols=[poscar_dict[s]],
                functional="PBE_64",
            )
            potcar.write_file("POTCAR.tmp")
            pv_potcar = PVPotcar("POTCAR.tmp")
            os.remove("POTCAR.tmp")
            metadata = pv_potcar.metadata
            titel = metadata.pop("TITEL")
            _type, _name, _date = titel.split()
            metadata["TYPE"] = _type
            metadata["NAME"] = _name
            metadata["DATE"] = _date
            data[s] = metadata

        # 创建 rich 表格
        table = Table(title="POTCAR Metadata", show_lines=False)

        # 添加列（第一列是参数名）
        table.add_column("Key", style="bold cyan")
        for element in data.keys():
            table.add_column(element, style="bold green")

        # 获取所有参数名（取并集）
        all_keys = sorted({k for v in data.values() for k in v.keys()})
        keys = all_keys

        for p in reversed(
            ["NAME", "TYPE", "DATE", "ENMIN", "ENMAX"]
        ):  # 反向插入，保持前后顺序
            if p in keys:
                keys.insert(0, keys.pop(keys.index(p)))

        # 填充行
        for key in keys:
            row = [key]
            for element in data.keys():
                val = data[element].get(key, "")
                if isinstance(val, list):
                    val = ", ".join(map(str, val))
                row.append(str(val))
            table.add_row(*row)

        # 输出表格
        console = Console()
        console.print(table)


if __name__ == "__main__":
    write_potcar_from_poscar("E:\WSL\dmft\POSCAR")
