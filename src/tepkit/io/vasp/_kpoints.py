from enum import StrEnum

import numpy as np
from tepkit.cli import logger
from tepkit.core.structure import abc_to_xyz
from tepkit.io import StructuredTextFile, array_to_string
from tepkit.utils.typing_tools import NumpyArray, NumpyArrayNx3, Self


class Kpoints(StructuredTextFile):
    """
    Ref:
    - https://www.vasp.at/wiki/index.php/KPOINTS
    """

    default_file_name = "KPOINTS"

    class Mode(StrEnum):
        """The Enum of all supported KPOINTS modes"""

        # Automatic / 自动生成 k 点
        Automatic = "Automatic"  # Deprecated
        Gamma = "Gamma"
        Monkhorst = "Monkhorst"
        # Explicit / 手动指定 k 点
        Cartesian = "Cartesian"  # xyz
        Fractional = "Fractional"  # abc
        # Line Mode
        Line = "Line"

        @classmethod
        def from_string(cls, string: str) -> Self:
            string = string.strip().capitalize()
            if string == "Reciprocal":
                return cls.Fractional
            return cls(string)

        def to_pymatgen(self):
            from pymatgen.io.vasp.inputs import KpointsSupportedModes

            replace_dict = {
                "Fractional": "Reciprocal",
                "Line": "Line_mode",
            }
            return KpointsSupportedModes[replace_dict.get(self.name, self.name)]

    def __init__(self):
        super().__init__()

        self.comment: str = "KPOINTS"
        """The 1st line: The comment line."""

    @staticmethod
    def get_2d_bz_kpoints(
        b_lattice,
        density: int = 10,
        edge_density: int = 15,
        scale: float = 1.0 + 1e-5,
        mode: str = "half",
    ):
        from matplotlib.patches import Polygon
        from tepkit.core.high_symmetry_points import HighSymmetryPoints2D
        from tepkit.core.structure import xyz_to_abc

        hsps = HighSymmetryPoints2D(b_lattice=b_lattice)
        df = hsps.get_boundary_df()
        bz = Polygon(
            df[["k_a", "k_b"]].values, edgecolor="black", facecolor="none"
        ).get_path()

        abc = []
        match density:
            case 0:
                abc.append((0.0, 0.0, 0.0))
            case n if isinstance(n, int) and n > 0:
                n = 2 * density + 1
                match mode:
                    case "full":
                        a_s = b_s = np.linspace(start=-1, stop=1, num=2 * n - 1)
                    case "half":
                        a_s = np.linspace(start=-1, stop=1, num=2 * n - 1)
                        b_s = np.linspace(start=0, stop=1, num=n)
                    case "quarter":
                        # TODO
                        raise NotImplementedError(
                            "The quarter style is not supported yet."
                        )
                    case _:
                        raise ValueError(f"Unknown style: {mode}.")
                for a in a_s:
                    for b in b_s:
                        if bz.contains_point((a / scale, b / scale)):
                            abc.append((a, b, 0.0))
            case _:
                raise Exception(
                    f"density can only be non-negative integer but not {density}."
                )
        abc = np.array(abc)

        kpoints_fill = ExplicitKpoints(
            comment=f"Fill(density={density})",
            mode=Kpoints.Mode.Fractional,
            kpts=abc,
            kpts_weights=[1] * len(abc),
        )

        # Path
        df = hsps.get_boundary_df(mode=mode)
        xyz = []
        distance1 = np.linalg.norm(df.iloc[0]["k_xyz"])
        for i in range(1, len(df)):
            xyz1 = df.iloc[i - 1]["k_xyz"]
            xyz2 = df.iloc[i]["k_xyz"]
            distance = np.linalg.norm(xyz2 - xyz1)
            num = int(distance / distance1 * edge_density) + 1
            xyz.append(np.linspace(start=xyz1, stop=xyz2, num=num, endpoint=False))
        xyz = np.concatenate(xyz)
        xyz = np.append(xyz, [df.iloc[-1]["k_xyz"]], axis=0)
        abc = xyz_to_abc(xyz, b_lattice)
        kpoints_edge = ExplicitKpoints(
            comment=f"Edge(density={edge_density})",
            mode=Kpoints.Mode.Fractional,
            kpts=abc,
            kpts_weights=[0] * len(abc),
        )

        # Result
        kpoints = kpoints_fill + kpoints_edge
        kpoints.b_lattice = b_lattice

        return kpoints


class ExplicitKpoints(Kpoints):
    """
    Ref:
    - https://www.vasp.at/wiki/index.php/KPOINTS
    """

    def __init__(
        self,
        mode: str | Kpoints.Mode,
        kpts: NumpyArrayNx3[float] | list[list[float]],
        kpts_weights: NumpyArray[float] | list[float],
        comment: str = "KPOINTS",
    ):
        super().__init__()
        self.comment = comment
        self.coordinates_mode: Kpoints.Mode = Kpoints.Mode.from_string(mode)
        """The coordinate mode. Cartesian or Reciprocal."""
        self.kpts: NumpyArrayNx3[float] = np.array(kpts)
        # Check and convert kpts_weights
        match kpts_weights:
            case n if isinstance(n, int) and n == 0:
                kpts_weights = [0] * len(kpts)
            case n if isinstance(n, int):
                raise ValueError(
                    "The value of kpts_weights can only be 0 or a integer list."
                )
            case n if len(n) != len(kpts):
                raise ValueError(
                    "The length of kpts_weights should be the same as kpts."
                )
            case _:
                pass
        self.kpts_weights: NumpyArray[float] = np.array(kpts_weights)
        self.b_lattice = None

    @property
    def num_kpts(self) -> int:
        return len(self.kpts)

    @property
    def df(self):
        import pandas as pd

        if self.coordinates_mode == self.Mode.Cartesian:
            xyz = self.kpts
        elif self.coordinates_mode == self.Mode.Fractional:
            if self.b_lattice is None:
                raise ValueError(
                    "Please set the ExplicitKpoints.b_lattice to use this property."
                )
            xyz = abc_to_xyz(self.kpts, self.b_lattice)
        else:
            raise ValueError(
                "The coordinates mode should be either 'Cartesian' or 'Reciprocal'."
            )

        df = pd.DataFrame(
            {
                "k_x": xyz[:, 0],
                "k_y": xyz[:, 1],
                "k_z": xyz[:, 2],
                "k_weight": self.kpts_weights,
            }
        )
        return df

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        从字符串中读取结构化数据。
        """
        lines = [line.strip() for line in string.splitlines()]
        comment = lines[0]
        num_kpts = int(lines[1])
        match num_kpts:
            case n if n < 0:
                # Invalid format.
                raise ValueError("The number of kpoints should be non-negative.")
            case 0:
                # Automatic generation kpoints.
                raise NotImplementedError(
                    "The automatic generation kpoints is not supported yet."
                )
            case n if n > 0:
                # Right result, continue.
                pass
            case _:
                # Should never reach here.
                raise Exception
        match lines[2].lower()[0]:
            case "l":
                # mode = cls.Mode.Line
                raise NotImplementedError("The line mode is not supported yet.")
            case "c" | "k":
                mode = cls.Mode.Cartesian
            case "f" | "r":
                mode = cls.Mode.Fractional
            case _:
                logger.warning(
                    f"Unknown coordinates mode: {lines[2]}, fallback to Reciprocal (Fractional) mode."
                )
                mode = cls.Mode.Fractional
        kpts = []
        kpts_weights = []
        for i in range(3, 3 + num_kpts):
            kpt_line = lines[i].split()
            kpt = [float(x) for x in kpt_line[:3]]
            kpt_weight = float(kpt_line[3])
            kpts.append(kpt)
            kpts_weights.append(kpt_weight)
        next_i = 3 + num_kpts
        if len(lines) > next_i:
            line = lines[next_i].strip()
            if line:
                if line[0].lower() == "t":
                    raise NotImplementedError(
                        "The tetrahedron method is not supported yet."
                    )
                else:
                    logger.warning(
                        f"Unknown content after all kpoints: {line}, ignored."
                    )
        return cls(
            mode=mode,
            kpts=kpts,
            kpts_weights=kpts_weights,
            comment=comment,
        )

    def __str__(self):
        kpts_lines = []
        for i, kpt in enumerate(self.kpts):
            kpts_line = (
                array_to_string(kpt, fmt="% 20.14f", delimiter="")
                + " " * 13
                + str(self.kpts_weights[i])
            )
            kpts_lines.append(kpts_line)
        blocks = [
            self.comment,
            str(self.num_kpts),
            self.coordinates_mode,
            "\n".join(kpts_lines),
        ]
        return "\n".join(blocks)

    def get_pymatgen_kpoints(self):
        from pymatgen.io.vasp import Kpoints as PymatgenKpoints
        from pymatgen.io.vasp.inputs import KpointsSupportedModes

        match self.coordinates_mode:
            case "Cartesian":
                mode = KpointsSupportedModes.Cartesian
            case "Reciprocal":
                mode = KpointsSupportedModes.Reciprocal
            case _:
                raise ValueError(
                    "The coordinates mode should be either 'Cartesian' or 'Reciprocal'."
                )

        return PymatgenKpoints(
            comment=self.comment,
            style=mode,
            num_kpts=self.num_kpts,
            kpts=self.kpts,
            kpts_weights=self.kpts_weights.tolist(),
        )

    def __add__(self, other):
        if self.coordinates_mode != other.coordinates_mode:
            raise ValueError(
                "The coordinates mode of the two kpoints should be the same."
            )
        result = ExplicitKpoints(
            mode=self.coordinates_mode,
            kpts=np.concatenate((self.kpts, other.kpts)),
            kpts_weights=np.concatenate((self.kpts_weights, other.kpts_weights)),
        )
        result.comment = self.comment + " + " + other.comment
        return result

    def plot(self, ax=None, show=False, save_path=None):
        from matplotlib import pyplot as plt
        from tepkit.utils.mpl_tools.plotters import (BrillouinZone2DPlotter,
                                                     ExplicitKpoints2DPlotter)

        if self.b_lattice is None:
            raise ValueError(
                "Please set the ExplicitKpoints.b_lattice to use this method."
            )
        pltr = BrillouinZone2DPlotter(b_lattice=self.b_lattice)
        pltr.base_vectors_length = 0.7
        if ax is None:
            fig, ax = plt.subplots()
        pltr.plot(ax)
        ExplicitKpoints2DPlotter(kpoints=self).plot(ax)
        ax.axis("equal")
        if show:
            plt.show()
        if save_path is not None:
            plt.savefig(save_path, dpi=300)
        return ax

    def show(self):
        self.plot(show=True)


class Ibzkpt(ExplicitKpoints):
    """
    Ref:
    - https://www.vasp.at/wiki/index.php/KPOINTS
    - https://www.vasp.at/wiki/index.php/IBZKPT
    """

    default_file_name = "IBZKPT"


if __name__ == "__main__":
    pass
