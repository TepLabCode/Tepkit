from tepkit.io.vasp import Poscar


def get_poscar_volume_cli(poscar="POSCAR"):
    poscar = Poscar.from_file(poscar)
    print(poscar.get_volume())
