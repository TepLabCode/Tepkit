import numpy as np

from tepkit.io.indices import TENSOR3D_ORDER3_INDICES
from tepkit.io import StructuredTextFile
from tepkit.utils.typing_tools import Self, NumpyArrayNx3, NumpyArray3
import pandas as pd


class ForceConstants3rd(StructuredTextFile):
    """
    3rd-order interatomic force constants file in ShengBTE format.
    """

    default_file_name = "FORCE_CONSTANTS_3RD"

    def __init__(self):
        super().__init__()
        self.df = None

    @classmethod
    def from_string(cls, string: str) -> Self:
        lines = string.splitlines()
        # 去除首两行，后每 32 (1+2+1+27+1) 行为一组
        data_groups: list[list[str]] = [
            lines[i : i + 32] for i in range(2, len(lines), 32)
        ]
        # 分析数据
        data_list = []
        for data_group in data_groups:
            index = int(data_group[0])
            atom_b_offset_xyz = np.array(data_group[1].split()).astype(float)
            atom_c_offset_xyz = np.array(data_group[2].split()).astype(float)
            uc_atom_indices = data_group[3].split()
            values = [line.split()[3] for line in data_group[4:31]]
            data_list.append(
                uc_atom_indices + [atom_b_offset_xyz, atom_c_offset_xyz] + values
            )
        # 创建 DataFrame
        df = pd.DataFrame(data_list)
        df.columns = (
            ["uc_atom_a", "uc_atom_b", "uc_atom_c"]
            + ["atom_b_offset_xyz", "atom_c_offset_xyz"]
            + TENSOR3D_ORDER3_INDICES
        )
        df.iloc[:, 0:3] = df.iloc[:, 0:3].astype(int)
        df.iloc[:, 5:] = df.iloc[:, 5:].astype(float)
        ifc3 = cls()
        ifc3.df = df
        return ifc3

    def calculate_rms(self) -> None:
        indices = TENSOR3D_ORDER3_INDICES
        self.df["rms"] = (
            self.df[indices].apply(lambda row: row.pow(2)).sum(axis=1) / 27
        ) ** 0.5

    def calculate_ion_positions(self, poscar) -> None:
        """计算原子在超胞中的位置"""
        df = self.df
        positions = poscar.get_cartesian_ion_positions()
        df["a_xyz"] = df.apply(lambda row: positions[row.uc_atom_a - 1], axis=1)
        df["b_xyz"] = df.apply(
            lambda row: positions[row.uc_atom_b - 1] + row.atom_b_offset_xyz, axis=1
        )
        df["c_xyz"] = df.apply(
            lambda row: positions[row.uc_atom_c - 1] + row.atom_c_offset_xyz, axis=1
        )
        pos_df = df[["a_xyz", "b_xyz", "c_xyz"]]
        pos_df = pos_df.map(lambda arr: np.where(np.abs(arr) < 1e-13, 0, arr))
        df[["a_xyz", "b_xyz", "c_xyz"]] = pos_df

    def calculate_ion_distances(self, sposcar) -> pd.DataFrame:
        """
        计算任意两原子间的距离
        """
        df = self.df
        if "a_xyz" not in df.columns:
            raise ValueError(
                "Must run ForceConstants3rd.calculate_ion_positions() first."
            )

        # 寻找最短距离
        import itertools

        row = df.shape[0]

        def get_min_distance(xyz1s, xyz2s):
            # print(type(xyz1s))  # <class 'pandas.core.series.Series'>
            # print(type(xyz1s.to_numpy()), xyz1s.shape)  # <class 'numpy.ndarray'> (N, 0)
            # print(np.stack(xyz1s.to_numpy()), xyz1s.shape) # <class 'numpy.ndarray'> (N, 3)
            xyz1s: NumpyArrayNx3 = np.stack(xyz1s.to_numpy())  # shape (N, 3)
            xyz2s: NumpyArrayNx3 = np.stack(xyz2s.to_numpy())  # shape (N, 3)
            distances = np.empty((row, 27))
            for i, offset in enumerate(itertools.product([-1, 0, 1], repeat=3)):
                offset_xyz: NumpyArray3 = np.dot(offset, sposcar.lattice)
                xyz2s_new: NumpyArrayNx3 = xyz2s + offset_xyz
                diff: NumpyArrayNx3 = xyz1s - xyz2s_new
                distances[:, i] = np.linalg.norm(diff, axis=1)  # shape (N, 27)
            return distances.min(axis=1)  # shape (N)

        df["d_ab"] = get_min_distance(df["a_xyz"], df["b_xyz"])
        df["d_ac"] = get_min_distance(df["a_xyz"], df["c_xyz"])
        df["d_bc"] = get_min_distance(df["b_xyz"], df["c_xyz"])
        df["d_min"] = df[["d_ab", "d_ac", "d_bc"]].min(axis=1)
        df["d_max"] = df[["d_ab", "d_ac", "d_bc"]].max(axis=1)
        df["d_avg"] = df[["d_ab", "d_ac", "d_bc"]].mean(axis=1)
        result_df = df[["d_ab", "d_ac", "d_bc", "d_min", "d_max", "d_avg"]]
        # result_df.to_csv("ion_distances.csv")
        return result_df


if __name__ == "__main__":
    from tepkit.io.vasp import Poscar
    from tepkit.io.phonopy import ForceConstants

    ifc2 = ForceConstants.from_file("_beta_data/FORCE_CONSTANTS_2ND")
    ifc2.df.to_csv("_beta_data/FORCE_CONSTANTS_2ND.csv")
    ifc3 = ForceConstants3rd.from_file("_beta_data/FORCE_CONSTANTS_3RD")
    ifc3.calculate_rms()
    ifc3.calculate_ion_positions(Poscar.from_file("_beta_data/POSCAR"))
    ifc3.df.to_csv("_beta_data/FORCE_CONSTANTS_3RD.csv")
    poscar = Poscar.from_file("_beta_data/3RD.SPOSCAR")
    print(poscar.get_cartesian_ion_positions(threshold=1e-13))
    from tepkit.functions.phonopy import rms

    # rms(
    #     work_dir="_beta_data",
    #     fc_name="FORCE_CONSTANTS_2ND",
    #     sposcar_name="SPOSCAR",
    #     xlim=None,
    #     ylim=None,
    # )

    # rms(
    #     work_dir="_beta_data",
    #     fc_name="FORCE_CONSTANTS_3RD",
    #     sposcar_name="3RD.SPOSCAR",
    #     xlim=None,
    #     ylim=None,
    #     fc3=True,
    # )

    # rms(
    #     work_dir="_beta_data/1/",
    #     save_dir="work_dir",
    #     fc_name="FORCE_CONSTANTS_3RD",
    #     sposcar_name="3RD.SPOSCAR",
    #     xlim=None,
    #     ylim=(1e-3, 10),
    #     fc3=True,
    #     log=True,
    # )
