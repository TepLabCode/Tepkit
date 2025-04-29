from enum import Enum
from typing import Optional

import numpy as np
from tepkit.io import StructuredTextFile, array_to_string, matrix_to_string
from tepkit.utils.typing_tools import NumpyArray3x3, NumpyArrayNx3, NumpyArrayNxN, Self


class VaspCoordinatesMode(str, Enum):
    Unknown = "Unknown"
    Fractional = "Direct"
    Direct = "Direct"
    Cartesian = "Cartesian"
    F = "Direct"
    D = "Direct"
    C = "Cartesian"


class Poscar(StructuredTextFile):
    """
    See: https://www.vasp.at/wiki/index.php/POSCAR
    """

    default_file_name = "POSCAR"

    def __init__(self):
        super().__init__()

        self.comment: str = "POSCAR"
        "The first line of POSCAR."

        self.scaling_factor: float | list[float] = 1.0
        self.unscale_lattice: Optional[NumpyArray3x3[float]] = None

        self.has_species_names: bool = True
        self.species_names: list[str] = []
        self.ions_per_species: list[int] = []

        self.ion_coordinates_mode: VaspCoordinatesMode = VaspCoordinatesMode.Unknown
        self.ion_positions: Optional[NumpyArrayNx3[float]] = None

        self.has_selective_dynamics: bool = False
        self.selective_dynamics: Optional[NumpyArrayNx3[bool]] = None

        self.has_lattice_velocities: bool = False
        self.lattice_velocities: Optional[NumpyArrayNx3[float]] = None

        self.has_ion_velocities: bool = False
        self.ion_velocities: Optional[NumpyArrayNx3[float]] = None

        self.md_extra: Optional[str] = None

    @classmethod
    def from_string(cls, string: str) -> Self:
        poscar = cls()
        lines = string.splitlines()
        index = 0

        # Comment
        poscar.comment = lines[index]
        index += 1

        # Scaling factor
        poscar.scaling_factor = np.array([float(x) for x in lines[index].split()])
        index += 1

        # Lattice
        poscar.unscale_lattice = np.empty((3, 3))
        for i in range(3):
            poscar.unscale_lattice[i] = [float(j) for j in lines[index + i].split()]
        index += 3

        # Species names (optional)
        if not lines[index].strip()[0].isdigit():  # 如果第一个字符不是数字
            poscar.species_names = lines[index].split()
            # TODO: 检查元素是否存在
            index += 1

        # Ions per species
        poscar.ions_per_species = np.array(lines[index].split()).astype(int)
        index += 1

        # Selective dynamics (optional)
        if lines[index].strip()[0] in ["S", "s"]:
            poscar.has_selective_dynamics = True
            index += 1
        else:
            poscar.has_selective_dynamics = False

        # Ion coordinates mode
        if lines[index].strip()[0] in ["C", "c", "K", "k"]:
            poscar.ion_coordinates_mode = VaspCoordinatesMode.C
        else:
            poscar.ion_coordinates_mode = VaspCoordinatesMode.F
        index += 1

        # Ion positions
        n_ions = poscar.ions_per_species.sum()
        poscar.ion_positions = np.empty((n_ions, 3))
        poscar.selective_dynamics = np.full((n_ions, 3), True, dtype=bool)
        for i in range(n_ions):
            poscar.ion_positions[i] = [float(j) for j in lines[index + i].split()[:3]]

        # Selective Dynamics
        if poscar.has_selective_dynamics:
            for i in range(n_ions):
                poscar.selective_dynamics[i] = [
                    cls._translate_selective_dynamics_flag(j)
                    for j in lines[index + i].split()[3:6]
                ]
        index += n_ions

        # TODO: self.has_lattice_velocities
        # TODO: self.lattice_velocities
        # TODO: self.has_ion_velocities
        # TODO: self.ion_velocities
        # TODO: self.md_extra

        return poscar

    def __str__(self):
        # ion_positions
        position_lines = [
            array_to_string(position, "%21.16f", prefix="  ")
            for position in self.ion_positions
        ]

        if self.has_selective_dynamics:
            for i in range(len(position_lines)):
                position_lines[i] += array_to_string(
                    self.selective_dynamics[i], fmt="bool_TF", prefix="  "
                )

        blocks = [
            self.comment,
            array_to_string(self.scaling_factor, prefix="  "),
            matrix_to_string(self.unscale_lattice, "%21.16f", line_prefix="  "),
            array_to_string(self.species_names, "%4s", prefix="  "),
            array_to_string(self.ions_per_species, "%4s", prefix="  "),
        ]
        blocks += ["Selective dynamics"] if self.has_selective_dynamics else []
        blocks += [
            "Direct",
            *position_lines,
        ]
        text = "\n".join(blocks)
        return text

    @staticmethod
    def _translate_selective_dynamics_flag(text: str) -> bool:
        if text == "T":
            return True
        elif text == "F":
            return False
        else:
            raise ValueError(
                f"selective_dynamics_flag can only be `T` or `F`, not {text}."
            )

    def get_lattice(self) -> NumpyArray3x3[float]:
        sf = self.scaling_factor
        match sf:
            case factor if len(sf) == 1 and sf >= 0:
                lattice = factor * self.unscale_lattice
            case volume if len(sf) == 1 and sf < 0:
                raise NotImplementedError(volume)
            case factors if len(factors) == 3 and np.all(factors >= 0):
                lattice = (self.unscale_lattice * factors).T
            case _:
                raise ValueError(
                    f"Scaling factor can only be [+float], [-float], or [+float，+float +float], but not {sf}."
                )
        return lattice

    def get_reciprocal_lattice(self, with_2pi=True) -> NumpyArray3x3[float]:
        """

        :param with_2pi: VASP Cartesian KPOINTS use with_2pi=False
        :return:
        """
        if with_2pi:
            return 2 * np.pi * np.linalg.inv(self.lattice).T
        else:
            return np.linalg.inv(self.lattice).T

    @property
    def lattice(self) -> NumpyArray3x3[float]:
        return self.get_lattice()

    @property
    def reciprocal_lattice(self) -> NumpyArray3x3[float]:
        return self.get_reciprocal_lattice()

    @property
    def n_ions(self) -> int:
        if sum(self.ions_per_species) == len(self.ion_positions):
            return sum(self.ions_per_species)
        else:
            raise ValueError("sum(self.ions_per_species) != len(self.positions)")

    @property
    def thickness_info(self) -> dict:
        """
        Returns thickness-related data.
        Such as effective thickness, van der Waals radius of edge atoms, etc.
        """
        import pandas as pd
        from mendeleev import element  # Cost time

        df = pd.DataFrame(self.get_cartesian_ion_positions())
        df.columns = ["x", "y", "z"]
        df["species_name"] = [
            self.species_names[i]
            for i, num in enumerate(self.ions_per_species)
            for _ in range(num)
        ]
        df = df.sort_values(by="z")
        cell_thickness = self.lattice[2][2]
        thickness = df["z"].max() - df["z"].min()
        element_bottom = df.iloc[0]["species_name"]
        element_top = df.iloc[-1]["species_name"]
        # Get the van der Waals radius of edge atoms (pm -> Angstrom)
        vdw_radius_bottom = element(element_bottom).vdw_radius / 100
        vdw_radius_top = element(element_top).vdw_radius / 100
        # Calculate effective thickness
        effective_thickness = vdw_radius_top + thickness + vdw_radius_bottom
        effective_thickness_proportion = effective_thickness / cell_thickness
        # Build result
        result = {
            "unit": "Angstrom",
            "cell_thickness": float(cell_thickness),
            "thickness": float(thickness),
            "element_top": element_top,
            "element_bottom": element_bottom,
            "vdw_radius_top": vdw_radius_top,
            "vdw_radius_bottom": vdw_radius_bottom,
            "effective_thickness": float(effective_thickness),
            "effective_thickness_proportion": float(effective_thickness_proportion),
        }
        # Return
        return result

    def get_cartesian_ion_positions(self) -> NumpyArrayNx3[float]:
        if self.ion_coordinates_mode == VaspCoordinatesMode.C:
            # Cartesian → Cartesian
            if self.scaling_factor == 1:
                return self.ion_positions
            else:
                raise NotImplementedError
        else:
            # Fractional -> Cartesian
            return np.matmul(self.ion_positions, self.lattice)

    def get_fractional_ion_positions(self) -> NumpyArrayNx3[float]:
        if self.ion_coordinates_mode == VaspCoordinatesMode.F:
            # Fractional → Fractional
            return self.ion_positions
        else:
            # Cartesian -> Fractional
            raise NotImplementedError

    def get_volume(self, unit: str = "Angstrom^3") -> float:
        volume = float(np.linalg.det(self.lattice))
        match unit:
            case "Angstrom^3" | "Å^3":
                return volume
            case "m^3" | "SI":
                return volume / 1e30
            case _:
                raise ValueError(
                    f"Unsupported unit: {unit}, only 'Angstrom^3', 'm^3', and 'SI' are supported."
                )

    def get_high_symmetry_points_2d(self, decimal, with_2pi=True):
        """
        Get the absolute and relative coordinates of all possible high symmetry points of a 2D material.

        :param decimal:
        :param with_2pi: VASP Cartesian KPOINTS use with_2pi=False
        :return:
        """
        from tepkit.core.high_symmetry_points import get_high_symmetry_points_2d

        b_lattice = self.get_reciprocal_lattice(with_2pi=with_2pi)
        return get_high_symmetry_points_2d(b_lattice=b_lattice, decimal=decimal)

    def get_interatomic_distances(self) -> NumpyArrayNxN[float]:
        """
        Return the distances between ions.
        """
        import itertools

        import scipy

        n_ions = self.n_ions
        ion_a_xyz = self.get_cartesian_ion_positions()
        distances = np.empty((27, n_ions, n_ions))
        for i, offset in enumerate(itertools.product([-1, 0, 1], repeat=3)):
            ion_b_xyz = np.dot(
                (self.get_fractional_ion_positions() + offset), self.lattice
            )
            distances[i, :, :] = scipy.spatial.distance.cdist(
                ion_a_xyz, ion_b_xyz, "euclidean"
            )
        min_distances = distances.min(axis=0)
        return min_distances

    def get_neighbor_distances(self, max_nth=100) -> list[float]:
        """
        Return the distances of the n-th neighbors.
        """
        from tqdm import tqdm

        distances = self.get_interatomic_distances()
        n_ions = distances.shape[0]
        ions_neighbor_distances = []
        for ion in tqdm(
            range(n_ions),
            bar_format=R"{l_bar}{bar}| [{n_fmt:>3}/{total_fmt:>3} Atoms]",
        ):
            # Distances
            ds = sorted(distances[ion, :])
            # Unique Distances
            uds = []
            breaked = False
            for d in ds:
                for ud in uds:
                    if np.allclose(ud, d):
                        break
                else:
                    uds.append(d)
                if len(uds) >= max_nth + 2:
                    breaked = True
                    break
            ion_neighbor_distances = [
                0.5 * (uds[i] + uds[i + 1]) for i in range(len(uds) - 1)
            ]
            if not breaked:
                ion_neighbor_distances.append(1.1 * max(uds))
            ions_neighbor_distances.append(ion_neighbor_distances)
        max_neighbor = min(len(nd) for nd in ions_neighbor_distances)
        all_ion_result = np.array(
            [ind[:max_neighbor] for ind in ions_neighbor_distances]
        )
        result = all_ion_result.max(axis=0)
        return result

    def get_atomic_numbers(self, per_ion=False) -> list[int]:
        """
        >>> poscar = Poscar.from_file("Bi2Te3.poscar")
        >>> poscar.get_atomic_numbers() # noinspection PyDocstringTypes
        [83, 52]
        >>> poscar.get_atomic_numbers(per_ion=True)
        [83, 83, 52, 52, 52]
        """
        from tepkit.core.atom import AtomicNumber

        numbers = [int(AtomicNumber[name]) for name in self.species_names]
        if not per_ion:
            return numbers
        else:
            if len(self.species_names) != len(self.ions_per_species):
                raise Exception("len(self.species_names) ≠ len(self.ions_per_species)")
            return [
                numbers[i]
                for i in range(len(self.species_names))  # 对每一个原子
                for _ in range(self.ions_per_species[i])  # 重复次数
            ]

    def get_pymatgen_poscar(self):
        # TODO
        pass

    def to_supercell(self, na: int, nb: int, nc: int) -> Self:
        sc = Poscar()
        sc.comment = f"The {na} x {nb} x {nc} supercell of {self.comment.strip()}"
        sc.scaling_factor = self.scaling_factor
        sc.unscale_lattice = self.unscale_lattice * (na, nb, nc)
        sc.has_species_names = self.has_species_names
        sc.species_names = self.species_names
        sc.ions_per_species = self.ions_per_species * na * nb * nc
        sc_positions = []
        for i in range(self.n_ions):
            uc_positions = self.ion_positions[i]
            for c in range(nc):
                for b in range(nb):
                    for a in range(na):
                        positions = (uc_positions + (a, b, c)) / (na, nb, nc)
                        sc_positions.append(positions)
        sc.ion_coordinates_mode = self.ion_coordinates_mode
        sc.ion_positions = np.vstack(sc_positions)
        return sc

    def get_shengbte_types(self, start=1):
        """
        返回每个原子的元素在元素列表的索引
        例： [0, 0, 1, 1, 2]
        """
        result = []
        for species in range(len(self.species_names)):
            for _ in range(self.ions_per_species[species]):
                result.append(species + start)
        return result


if __name__ == "__main__":
    pass
