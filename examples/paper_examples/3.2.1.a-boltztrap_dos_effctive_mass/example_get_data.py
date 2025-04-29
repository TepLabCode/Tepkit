from pathlib import Path

from tepkit.io.boltztrap2 import Condtens
from tepkit.io.vasp import Poscar

path = Path("input-boltztrap2")
condtens = Condtens.from_dir(path)
poscar = Poscar.from_dir(path)
lattice = poscar.get_lattice()
condtens.calculate_average_effective_mass(
    "m_e",
    volume=poscar.get_volume(unit="m^3"),
)
condtens.df.to_csv("condtens_with_eff_mass.csv")
