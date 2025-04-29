import numpy as np
import pandas as pd

from tepkit.core.geometry import Point2D, mid_line, cross_point
from tepkit.core.structure import abc_to_xyz, xyz_to_abc
from tepkit.core.symmetry import BravaisLattice2D
from tepkit.core.symmetry_data import (
    high_symmetry_paths_data,
    high_symmetry_points_text_data,
)
from tepkit.utils.typing_tools import NumpyArray3x3

high_symmetry_points_2d_tokens: list[str] = (
    # 固定 k_abc
    ["G"]  # 中心点
    + ["A", "AR"]  # ± b1 / 2 (R for Reverse)
    + ["B", "BR"]  # ± b2 / 2 (R for Reverse)
    + ["C1", "C2", "C3", "C4"]  # ± (b1 ± b2) / 2
    # 动态 k_abc
    # b1 b2 中垂线 与 b1+b2 中垂线的交点
    + ["C1A", "C1B", "C2A", "C2B", "C3A", "C3B", "C4A", "C4B"]
    # b1 与 b2 中垂线的交点
    + ["D1", "D2", "D3", "D4"]
)
R"""
The unique names of 2D high symmetry points.

::

    +---------------------+---------------------+
    | Overview:           |  Right (=90):       |
    | D2  C2B B  C1B D1   |  D2------B------D1  |
    |   C2         C1     |  |       |      |   |
    | C2A            C1A  |  |       |      |   |
    | AR      G      A    |  AR      G------A   |
    | C3A            C4A  |  |              |   |
    |   C3         C4     |  |              |   |
    | D3  C3B BR C4B D4   |  D3------BR-----D4  |
    +---------------------+---------------------+
    | Acute (<90):        |  Obtuse (>90):      |
    |     C2B----B---D1   |  D2---B-----C1B     |
    |   C2      /    |    |  |     \      C1    |
    | C2A      /     |    |  |      \       C1A |
    | AR      G------A    |  AR      G------A   |
    | |              C4A  |  C3A            |   |
    | |            C4     |    C3           |   |
    | D3---BR----C4B      |      C3B----BR--D4  |
    +---------------------+---------------------+

"""


def get_high_symmetry_points_2d(
    b_lattice: NumpyArray3x3,
    *,
    decimal: int = 10,
    combine: bool = True,
    split: bool = False,
) -> pd.DataFrame:
    """
    Get the absolute and relative coordinates of all possible high symmetry points of a 2D material.

    :param b_lattice: The reciprocal lattice of the strcture.
    :param decimal: Used to eliminate minor errors caused by binary. (like 0.9999 or 1e-11)
    :param combine: If True, the dataframe will inclue ["k_abc", "k_xyz"] columns.
    :param split: If True, the dataframe will inclue ["k_a", "k_b", "k_c"] and ["k_x", "k_y", "k_z"] columns.
    """
    # Initalization / 初始化
    lattice = b_lattice
    data = {
        "token": high_symmetry_points_2d_tokens,
        "k_abc": [None] * len(high_symmetry_points_2d_tokens),
        "k_xyz": [None] * len(high_symmetry_points_2d_tokens),
    }
    df = pd.DataFrame(data)
    df.set_index("token", inplace=True)
    b1 = lattice[0][:2]
    b2 = lattice[1][:2]

    # 已知 abc 求 xyz
    fixed_k_abc = {
        "G":  (   0,    0, 0),
        "A":  (+0.5,    0, 0),
        "AR": (-0.5,    0, 0),
        "B":  (   0, +0.5, 0),
        "BR": (   0, -0.5, 0),
        "C1": (+0.5, +0.5, 0),
        "C2": (-0.5, +0.5, 0),
        "C3": (-0.5, -0.5, 0),
        "C4": (+0.5, -0.5, 0),
    }  # fmt: skip

    for token, k_abc in fixed_k_abc.items():
        k_abc = np.array(k_abc)
        df.at[token, "k_abc"] = k_abc
        df.at[token, "k_xyz"] = abc_to_xyz(k_abc, lattice)

    # 求解其他点的 xy
    points = {
        "g": Point2D(0, 0),
        "b1": Point2D(*b1),
        "b2": Point2D(*b2),
    }
    lattice_points = {
        "A": +points["b1"],
        "B": +points["b2"],
        "AR": -points["b1"],
        "BR": -points["b2"],
        "C1": +points["b1"] + points["b2"],
        "C2": -points["b1"] + points["b2"],
        "C3": -points["b1"] - points["b2"],
        "C4": +points["b1"] - points["b2"],
    }
    # 计算中垂线
    mid_lines = {
        key: mid_line(points["g"], value) for key, value in lattice_points.items()
    }
    # 计算中垂线交点
    cross_points = {
        "C1A": (mid_lines["C1"], mid_lines["A"]),
        "C1B": (mid_lines["C1"], mid_lines["B"]),
        "C2A": (mid_lines["C2"], mid_lines["AR"]),
        "C2B": (mid_lines["C2"], mid_lines["B"]),
        "C3A": (mid_lines["C3"], mid_lines["AR"]),
        "C3B": (mid_lines["C3"], mid_lines["BR"]),
        "C4A": (mid_lines["C4"], mid_lines["A"]),
        "C4B": (mid_lines["C4"], mid_lines["BR"]),
        "D1": (mid_lines["A"], mid_lines["B"]),
        "D2": (mid_lines["B"], mid_lines["AR"]),
        "D3": (mid_lines["AR"], mid_lines["BR"]),
        "D4": (mid_lines["BR"], mid_lines["A"]),
    }
    k_xys = {
        key: tuple(cross_point(values[0], values[1], decimal=decimal))
        for key, values in cross_points.items()
    }

    # 已知 xyz 求 abc
    for name, k_xy in k_xys.items():
        k_xyz = (*k_xy, 0)
        k_xyz = np.array(k_xyz)
        df.at[name, "k_xyz"] = k_xyz
        df.at[name, "k_abc"] = xyz_to_abc(k_xyz, lattice, decimal=decimal)

    if split:
        df[["k_a", "k_b", "k_c"]] = pd.DataFrame(df["k_abc"].tolist(), index=df.index)
        df[["k_x", "k_y", "k_z"]] = pd.DataFrame(df["k_xyz"].tolist(), index=df.index)
    if not combine:
        df.drop(columns=["k_abc", "k_xyz"], inplace=True)
    # Return
    return df


class HighSymmetryPoints2D:
    """
    A class to manage the high symmetry points of a 2D material.
    """

    boundary_tokens_dict = {
        # 直角
        "right": ["A", "D1", "B", "D2", "AR", "D3", "BR", "D4", "A"],
        # 锐角
        "acute": ["A", "D1", "B", "C2B", "C2A", "AR", "D3", "BR", "C4B", "C4A", "A"],
        # 钝角
        "obtuse": ["A", "C1A", "C1B", "B", "D2", "AR", "C3A", "C3B", "BR", "D4", "A"],
    }

    half_boundary_tokens_dict = {
        "right": ["A", "D1", "B", "D2", "AR"],
        "acute": ["A", "D1", "B", "C2B", "C2", "C2A", "AR"],
        "obtuse": ["A", "C1A", "C1", "C1B", "B", "D2", "AR"],
    }
    """Used for get_2d_bz_kpoints() method."""

    right_angle_precision = 1e-3
    default_text_style = "Setyawan2010_tex"
    default_path_style = "Setyawan2010"

    def __init__(
        self,
        b_lattice: NumpyArray3x3,
        bravais_lattice_2d=None,
        text_style: str = None,
        path_style: str = None,
    ):
        self._lattice: NumpyArray3x3 = b_lattice
        """
        obj._lattice can only be assigned a value during init.
        Modifying it at any other time may produce incorrect results.
        """
        self.path_style = path_style or self.default_path_style
        """
        The style of the choices of the high symmetry paths.
        obj.path_style = Setyawan2010 / Tepkit2024
        """
        self.text_style = text_style or self.default_text_style
        """
        The style of the names of the high symmetry points.
        obj.text_style = Setyawan2010 / Setyawan2010_tex / Tepkit2024 / Tepkit2024_tex
        """
        self.df = get_high_symmetry_points_2d(
            b_lattice=self._lattice,
            combine=True,
            split=True,
        )
        """
        obj.df = pd.DataFrame
        """
        self.bravais_lattice_2d: BravaisLattice2D = bravais_lattice_2d
        self._gamma_type = self.get_gamma_angle_type()
        """
        obj._gamma_type = right / acute / obtuse
        """

    class LatticeGammaException(Exception):
        pass

    @property
    def lattice_gamma_type(self):
        if self.bravais_lattice_2d is None:
            raise self.LatticeGammaException(
                "You must assign HighSymmetryPoints2D.bravais_lattice_2d \
                 to get the lattice_gamma_type."
            )
        return self.bravais_lattice_2d, self._gamma_type

    @classmethod
    def from_poscar(
        cls,
        poscar,
        with_2pi: bool = True,
        text_style: str = None,
        path_style: str = None,
    ):
        """
        Instantiation a Plotter by a Poscar.
        """
        obj = cls(
            b_lattice=poscar.get_reciprocal_lattice(with_2pi=with_2pi),
            bravais_lattice_2d=BravaisLattice2D.from_poscar(poscar),
            text_style=text_style,
            path_style=path_style,
        )
        return obj

    def add_token_texts(self):
        pass

    def get_gamma_angle_type(self):
        """
        计算倒晶格 gamma 角的类型
        """
        b1 = self._lattice[0][:2]
        b2 = self._lattice[1][:2]
        match np.dot(b1, b2):
            case x if abs(
                x / np.linalg.norm(b1) / np.linalg.norm(b2)
            ) < self.right_angle_precision:
                angle = "right"
            case x if x > 0:
                angle = "acute"
            case x if x < 0:
                angle = "obtuse"
            case _:
                raise Exception
        return angle

    def get_boundary_tokens(self, mode="full") -> list[str]:
        match mode:
            case "full":
                return self.boundary_tokens_dict[self._gamma_type]
            case "half":
                return self.half_boundary_tokens_dict[self._gamma_type]
            case _:
                raise Exception(f"Invalid mode {mode}.")

    def get_boundary_df(self, mode="full"):
        return self.df.loc[self.get_boundary_tokens(mode=mode)]

    class GammaAngleException(Exception):
        pass

    def get_paths_tokens(self) -> list[list[str]]:
        """
        根据晶格类型和角度的组合自动获取高对称路径数据。
        :return: e.g. [["G", "D1", "B", "C2B", "C2", "G"]]
        """
        lattice_type = self.lattice_gamma_type
        data = high_symmetry_paths_data["Setyawan2010"]
        if lattice_type in data:
            tokens = data[lattice_type]
        elif lattice_type == (BravaisLattice2D.oc, "right"):
            if self._lattice[0][0] == self._lattice[1][1]:
                raise self.GammaAngleException(
                    "Your square cell (a1 = a2, γ = 90°) is not consistant with the centered-rectangular (oc) symmetry."
                )
            else:
                raise Exception(
                    "Please use the rhombus primitive cell (a1 = a2, γ ≠ 90°) "
                    "for the centered-rectangular (oc) lattice."
                )
        else:
            raise self.GammaAngleException(
                f"Invalid Bravais lattice type `{self.bravais_lattice_2d}` "
                f"with the gamma angle `{self._gamma_type}`."
            )
        return tokens

    def get_paths_df(self):
        # TODO: MUlti-path
        return self.df.loc[self.get_paths_tokens()[0]]

    def get_df_by_tokens(self, tokens: list[str] | None = None):
        if tokens:
            return self.df.loc[tokens]
        return self.df

    def get_dict(
        self,
        key_column: str = None,
        value_column: str = None,
        tokens: list[str] = None,
    ) -> dict:
        df = self.get_df_by_tokens(tokens)
        if tokens is not None:
            if len(tokens) != len(set(tokens)):
                # TODO warning
                pass
        keys = self.get_list(key_column, tokens)
        values = self.get_list(value_column, tokens)
        return dict(zip(keys, values))

    def get_list(self, column=None, tokens=None) -> list:
        if column == "text":
            return self.get_texts(tokens)
        df = self.get_df_by_tokens(tokens)
        if column == "token":
            return df.index.tolist()
        elif column == "k_xy":
            return df["k_xyz"].apply(lambda x: x[:2]).tolist()
        return df[column].tolist()

    def get_texts(self, tokens):
        tokens = self.get_list("token", tokens)
        if self.text_style.startswith("Setyawan2010"):
            lattice_type = self.lattice_gamma_type
            data = high_symmetry_points_text_data["Setyawan2010"]
            if lattice_type in data:
                replace_texts = data[lattice_type]
            else:
                replace_texts = {}
            texts = [replace_texts.get(token, token) for token in tokens]
        elif self.text_style.startswith("Tepkit2024"):
            texts = tokens

        # Subscript for TeX style
        if self.text_style.endswith("_tex"):

            def get_tex_text(text):
                if len(text) == 1:
                    return R"$\mathrm{" + text + "}$"
                else:
                    return R"$\mathrm{" + text[0] + "}_{" + text[1:] + "}$"

            texts = [get_tex_text(text) for text in texts]

        return texts


if __name__ == "__main__":

    def _test():
        test_lattice = [
            [1, -1.2, 0],
            [1, 1.2, 0],
            [0, 0, 10],
        ]
        test_lattice = 2 * np.pi * np.linalg.inv(test_lattice).T
        test_df = get_high_symmetry_points_2d(test_lattice)
        print(test_df)
        print(test_df["k_xyz"].to_dict())
        data = test_df["k_xyz"].values
        data_array = np.array([np.array(item) for item in data])
        print(data_array)
        print(type(test_df["k_xyz"].values))

        setyawan2010style = {
            # Square (tp)
            # ├ A.4. Tetragonal (TET, tP) | Fig.4 | Table 5
            # └ a-right/b-right
            BravaisLattice2D.tp: {
                "labels": ["G", "X", "M", "G"],
                "tokens": ["G", "A", "D1", "G"],
            },
            # Rectangular (op)
            # ├ A.6. Orthorhombic (ORC, oP) | Fig.7 | Table 8
            # └ a1 < a2 | a-right/b-right
            BravaisLattice2D.op: {
                "labels": ["G", "X", "S", "Y", "G"],
                "tokens": ["G", "A", "D1", "B", "G"],
            },
            # Centered rectangular (oc)
            # ├ A.9. C-centered orthorhombic (ORCC, oS) | Fig.12 | Table 12
            # └ a < b | a1 = (a/2, b/2, 0) | a2 = (a/2, b/2, 0) | => a-obtuse/b-acute
            BravaisLattice2D.oc: {
                "labels": ["G", "X", "S", "X1", "Y", "G"],
                "tokens": ["G", "D1", "BR", "C2B", "D2", "G"],
            },
            # Hexagonal (hp)
            # ├ A.10. Hexagonal (HEX, hP) | Fig. 13 | Table 13
            # └ a1 = (a/2, -√3/2 a, 0) | a2 = (a/2, √3/2 a, 0) | => a-obtuse/b-acute
            BravaisLattice2D.hp: {
                "labels": ["G", "M", "K", "G"],
                "tokens": ["G", "A", "D1", "G"],
            },
            # Oblique (mp)
            # ├ A.12. Monoclinic (MCL, mP) | Fig.16 | Table 16
            # └ α < 90° => a-acute/b-obtuse
            (BravaisLattice2D.mp, "obtuse"): {
                "labels": ["G", "X", "H1", "C", "H", "Y", "G", "C"],
                "tokens": ["G", "A", "C1A", "C1", "C1B", "B", "G", "C1"],
            },
            (BravaisLattice2D.mp, "acute"): {
                "labels": ["G", "X", "H1", "C", "H", "Y", "G", "C"],
                "tokens": ["G", "AR", "C2A", "C2", "C2B", "B", "G", "C2"],
            },
        }
        """
        https://linkinghub.elsevier.com/retrieve/pii/S0927025610002697
        [1] W. Setyawan and S. Curtarolo, High-throughput electronic band structure calculations: Challenges and tools,
            Comput. Mater. Sci. 49, 299 (2010).
        """
        print(setyawan2010style)
