from tepkit.io.indices import T3D_INDICES
from tepkit.io import StructuredTextFile
from tepkit.utils.typing_tools import Self
import pandas as pd


class ForceConstants(StructuredTextFile):
    """
    2nd-order interatomic force constants file in Phonopy format.
    """

    default_file_name = "FORCE_CONSTANTS"

    def __init__(self):
        super().__init__()
        self.df = None

    @classmethod
    def from_string(cls, string: str) -> Self:
        ifc2 = cls()
        lines = string.splitlines()
        # 去除首行，后每 4 行为一组
        data_groups = [" ".join(lines[i : i + 4]) for i in range(1, len(lines), 4)]
        # 分列每组数据，得到二维列表
        data_list = [i.split() for i in data_groups]
        # 创建 DataFrame
        df = pd.DataFrame(data_list)
        df.iloc[:, 0:2] = df.iloc[:, 0:2].astype(int)
        df.iloc[:, 2:] = df.iloc[:, 2:].astype(float)
        df.columns = ["atom_a", "atom_b"] + T3D_INDICES
        ifc2.df = df
        return ifc2
