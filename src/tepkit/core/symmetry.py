from typing import Type

from tepkit.io.vasp import Poscar
from enum import Enum, StrEnum

from tepkit.utils.typing_tools import Self


class Axis(int, Enum):
    a1 = 0
    a2 = 1
    a3 = 2


class BravaisSystem2D(StrEnum):
    Oblique = "Oblique (m)"
    Rectangular = "Rectangular (o)"
    Square = "Square (t)"
    Hexagonal = "Hexagonal (h)"


class BravaisLattice2D(StrEnum):
    """
    >>> BravaisLattice2D.mp
    'mp'
    """

    mp = "mp"
    """ Oblique """
    op = "op"
    """ Rectangular """
    oc = "oc"
    """ Centered-Rectangular """
    tp = "tp"
    """ Square """
    hp = "hp"
    """ Hexagonal """

    @classmethod
    def from_string(cls, key) -> Self:
        key = key.lower()
        if key in ["mp", "obl", "oblique"]:
            return cls.mp
        elif key in ["op", "rec", "rectangular"]:
            return cls.op
        elif key in ["oc", "cen", "centered-rectangular", "rho", "rhombus"]:
            return cls.oc
        elif key in ["tp", "squ", "square"]:
            return cls.tp
        elif key in ["hp", "hex", "hexagonal"]:
            return cls.hp
        else:
            raise KeyError(f"{key} is not a valid BravaisLattice2D key")

    @classmethod
    def keys(cls) -> list[str]:
        return (
            ["mp", "obl", "oblique"]
            + ["op", "rec", "rectangular"]
            + ["oc", "cen", "centered-rectangular", "rho", "rhombus"]
            + ["tp", "squ", "square"]
            + ["hp", "hex", "hexagonal"]
        )

    @property
    def long_name(self) -> str:
        match self:
            case BravaisLattice2D.mp:
                return "Oblique"
            case BravaisLattice2D.op:
                return "Rectangular"
            case BravaisLattice2D.oc:
                return "Centered-Rectangular"
            case BravaisLattice2D.tp:
                return "Square"
            case BravaisLattice2D.hp:
                return "Hexagonal"
        return "Unknown"

    def to_string(self, style) -> str:
        match style:
            case "short":
                return self.name
            case "long":
                return self.long_name
            case "full":
                return f"{self.long_name} ({self.name})"

    @classmethod
    def differentiate_rectangular_lattice(cls, space_group_number: int) -> Self:
        oc_numbers = [20, 21] + [35, 36, 37, 38, 39, 40, 41] + [63, 64, 65, 66, 67]
        op_numbers = (
            [16, 17, 18, 19]
            + [25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
            + [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]
        )
        op_numbers += [3, 4, 6, 7, 10, 11, 13, 14]  # mP
        if space_group_number in oc_numbers:
            return cls.oc
        elif space_group_number in op_numbers:
            return cls.op
        else:
            raise Exception(
                f"Invalid space group number {space_group_number} for 2D rectangular lattice."
            )

    @classmethod
    def from_bravais_system_2d(
        cls,
        bravais_system_2d: BravaisSystem2D,
        sg_number=None,
    ) -> Self:
        match bravais_system_2d:
            case BravaisSystem2D.Oblique:
                return cls.mp
            case BravaisSystem2D.Rectangular:
                return cls.differentiate_rectangular_lattice(sg_number)
            case BravaisSystem2D.Square:
                return cls.tp
            case BravaisSystem2D.Hexagonal:
                return cls.hp

    @classmethod
    def from_file(cls, path, fmt, sym_prec=1e-5) -> Self:
        data = LayerGroup.from_file(path, fmt, sym_prec=sym_prec).data
        bravais_system = data["bravais_system_2d"]
        sg_number = data["sg_number"]
        return cls.from_bravais_system_2d(bravais_system, sg_number)

    @classmethod
    def from_poscar(cls, poscar, sym_prec=1e-5) -> Self:
        data = LayerGroup.from_poscar(poscar, sym_prec=sym_prec).data
        bravais_system = data["bravais_system_2d"]
        sg_number = data["sg_number"]
        return cls.from_bravais_system_2d(bravais_system, sg_number)


class CrystalSystem3D(StrEnum):
    Triclinic = "Triclinic"
    Monoclinic = "Monoclinic"
    Orthorhombic = "Orthorhombic"
    Tetragonal = "Tetragonal"
    Trigonal = "Trigonal"
    Hexagonal = "Hexagonal"


class LayerGroup:
    def __init__(self):
        self.data = None

    @classmethod
    def from_file(
        cls,
        path,
        fmt,
        aperiodic_axis: Axis | Type[Axis] = Axis.a3,
        sym_prec: float = 1e-5,
    ):
        """
        >>> layer_group = LayerGroup.from_file("Bi2Te3.poscar", fmt="vasp")
        >>> layer_group.number
        72
        >>> layer_group.data.international
        'p-3m1'
        """
        match fmt.lower():
            case "vasp" | "poscar":
                poscar = Poscar.from_file(path)
                return cls.from_poscar(
                    poscar=poscar,
                    aperiodic_axis=aperiodic_axis,
                    sym_prec=sym_prec,
                )
            case _:
                raise NotImplementedError("Only support VASP(POSCAR) format now.")

    @classmethod
    def from_poscar(
        cls,
        poscar: Poscar,
        aperiodic_axis: Axis = Axis.a3,
        sym_prec: float = 1e-5,
    ):
        obj = cls()
        lattice = poscar.lattice
        positions = poscar.get_fractional_ion_positions()
        numbers = poscar.get_atomic_numbers(per_ion=True)
        cell = (lattice, positions, numbers)
        obj.get_data_from_spglib(cell, aperiodic_axis, sym_prec)
        return obj

    def get_data_from_spglib(
        self,
        cell,
        aperiodic_axis: Axis = Axis.a3,
        sym_prec: float = 1e-5,
    ):
        import dataclasses
        from spglib.spglib import get_symmetry_layerdataset, get_symmetry_dataset

        data = get_symmetry_layerdataset(
            cell,
            aperiodic_dir=aperiodic_axis,
            symprec=sym_prec,
        )
        data = dataclasses.asdict(data)
        sg_data = get_symmetry_dataset(
            cell,
            symprec=sym_prec,
        )
        sg_data = dataclasses.asdict(sg_data)
        data["sg_number"] = sg_data["number"]
        data["sg_international"] = sg_data["international"]

        self.data = data
        self.add_additional_data()

    @property
    def number(self) -> int:
        if self.data is None:
            raise AttributeError("No Layer Group Data Found.")
        return self.data["number"]

    def add_additional_data(self) -> None:
        match self.number:
            case n if 1 <= n <= 2:
                bravais_system_2d = BravaisSystem2D.Oblique
                crystal_system_3d = CrystalSystem3D.Triclinic
            case n if 3 <= n <= 7:
                bravais_system_2d = BravaisSystem2D.Oblique
                crystal_system_3d = CrystalSystem3D.Monoclinic
            case n if 8 <= n <= 18:
                bravais_system_2d = BravaisSystem2D.Rectangular
                crystal_system_3d = CrystalSystem3D.Monoclinic
            case n if 19 <= n <= 48:
                bravais_system_2d = BravaisSystem2D.Rectangular
                crystal_system_3d = CrystalSystem3D.Orthorhombic
            case n if 49 <= n <= 64:
                bravais_system_2d = BravaisSystem2D.Square
                crystal_system_3d = CrystalSystem3D.Tetragonal
            case n if 65 <= n <= 72:
                bravais_system_2d = BravaisSystem2D.Hexagonal
                crystal_system_3d = CrystalSystem3D.Trigonal
            case n if 73 <= n <= 80:
                bravais_system_2d = BravaisSystem2D.Hexagonal
                crystal_system_3d = CrystalSystem3D.Hexagonal
            case _:
                raise Exception(f"Invalid layer group number {self.number}")
        self.data["bravais_system_2d"] = bravais_system_2d
        self.data["crystal_system_3d"] = crystal_system_3d
