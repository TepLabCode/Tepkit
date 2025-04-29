from collections import OrderedDict

import numpy as np
from tepkit.io import StructuredTextFile
from tepkit.io.vasp import Poscar
from tepkit.utils.typing_tools import Self


class Control(StructuredTextFile):
    """
    For ShengBTE input file ``CONTROL`` .

    Supported Files
    ===============
    - CONTROL
    """

    default_file_name = "CONTROL"

    def __init__(self):
        super().__init__()
        self.data = OrderedDict(
            {
                "allocations": OrderedDict(),
                "crystal": OrderedDict(),
                "parameters": OrderedDict(),
                "flags": OrderedDict(),
            }
        )
        self.data["parameters"]["scalebroad"] = 1.0
        self.data["parameters"]["nticks"] = 100
        self.scell = np.array((1, 1, 1))
        self.ngrid = np.array((1, 1, 1))
        self.temperature = 300

    @classmethod
    def from_poscar(cls, path) -> Self:
        control = cls()
        poscar = Poscar.from_file(path)
        # allocations
        control.data["allocations"]["nelements"] = len(poscar.species_names)
        control.data["allocations"]["natoms"] = len(poscar.ion_positions)
        # crystal
        # 0.1 measns Angstrom (in VASP) to nm (in ShengBTE)
        control.data["crystal"]["lfactor"] = 0.1
        control.data["crystal"]["lattvec"] = poscar.get_lattice()
        control.data["crystal"]["elements"] = poscar.species_names
        control.data["crystal"]["types"] = poscar.get_shengbte_types(start=1)
        control.data["crystal"]["positions"] = poscar.ion_positions
        return control

    @property
    def namelist(self):
        import f90nml

        namelist = f90nml.Namelist(self.data)
        namelist.float_format = " .16f"
        return namelist

    def __str__(self):
        return str(self.namelist)

    def write(self, path="./CONTROL.nml", force=True):
        self.namelist.write(path, force=force)

    # === Shortcuts for some parameters === #
    @property
    def ngrid(self):
        return self.data["allocations"]["ngrid"]

    @ngrid.setter
    def ngrid(self, value):
        self.data["allocations"]["ngrid"] = np.array(value)

    @property
    def scell(self):
        return self.data["crystal"]["scell"]

    @scell.setter
    def scell(self, value):
        self.data["crystal"]["scell"] = np.array(value)

    @property
    def temperature(self):
        return self.data["parameters"].get("T")

    @temperature.setter
    def temperature(self, value):
        self.data["parameters"].pop("T_min", None)
        self.data["parameters"].pop("T_max", None)
        self.data["parameters"].pop("T_step", None)
        self.data["parameters"]["T"] = value

    @property
    def temperatures(self):
        return (
            self.data["parameters"]["T_min"],
            self.data["parameters"]["T_max"],
            self.data["parameters"]["T_step"],
        )

    @temperatures.setter
    def temperatures(self, value):
        self.data["parameters"].pop("T", None)
        self.data["parameters"]["T_min"] = value[0]
        self.data["parameters"]["T_max"] = value[1]
        self.data["parameters"]["T_step"] = value[2]


if __name__ == "__main__":
    obj = Control.from_poscar("../vasp/test.poscar")
    obj.write()
