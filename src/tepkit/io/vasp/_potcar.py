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


def write_potcar_from_poscar(poscar_path="POSCAR", *, potcar_path="POTCAR"):
    from pymatgen.io.vasp import Poscar, Potcar

    poscar = Poscar.from_file(poscar_path)
    poscar_dict = VASP_RECOMMENDED_POTENTIALS_PAW_PBE_64
    pot_symbols = [poscar_dict[s] for s in poscar.site_symbols]
    potcar = Potcar(
        symbols=pot_symbols,
        functional="PBE_64",
    )
    potcar.write_file(potcar_path)
