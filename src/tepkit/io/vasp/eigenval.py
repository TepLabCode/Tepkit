import pandas as pd
from tepkit.io import StructuredTextFile
from tepkit.utils.typing_tools import Self


class Eigenval(StructuredTextFile):
    """
    The class of EIGENVAL file for VASP.

    **Refs:**

    - https://www.vasp.at/wiki/index.php/EIGENVAL
    - https://www.vasp.at/wiki/index.php/DOSCAR
    - https://w.vasp.at/forum/viewtopic.php?p=20810
    - https://sisl.readthedocs.io/en/latest/_modules/sisl/io/vasp/eigenval.html
    """

    default_file_name = "EIGENVAL"
    data_columns = {
        False: ["energy", "fermi_weight"],
        True: ["energy_1", "energy_2", "fermi_weight_1", "fermi_weight_2"],
    }

    def __init__(self):
        super().__init__()
        self.data = {}
        self.extra_data = {}
        self.df = None
        self.soc: bool = None

    @classmethod
    def from_string(cls, string: str) -> Self:
        eigenval = cls()
        lines = string.splitlines()
        # 错误处理
        if len(lines) < 8:
            raise ValueError("The EIGENVAL file is incomplete.")
        # Read Line 1 Data
        line_data = lines[0].split()
        eigenval.data.update(
            {
                "NIONS (Including empty spheres)": int(line_data[0]),
                "NIONS": int(line_data[0]),
                "NBLOCK * KBLOCK": int(line_data[2]),
                "ISPIN": int(line_data[3]),
            }
        )
        # Read Line 2 Data
        line_data = lines[1].split()
        eigenval.data.update(
            {
                # Volume per Atom (Å)
                "AOMEGA": float(line_data[0]),
                # Length of the Basis (m -> Å)
                "ANORM": [float(_) * 1e10 for _ in line_data[1:4]],
                # POTIM (s -> fs)
                "POTIM": float(line_data[4]) * 1e15,
            }
        )
        # Read Line 3 Data
        eigenval.data["TEMP"] = float(lines[2].strip())
        # Read Line 4 Data
        eigenval.data["LINE_4"] = "  CAR "
        # Read Line 5 Data
        eigenval.data["SYSTEM"] = lines[4].strip()
        # Read Line 6 Data
        line_data = lines[5].split()
        eigenval.data.update(
            {
                "n_electrons": int(line_data[0]),
                "n_kpoints": int(line_data[1]),
                "n_bands": int(line_data[2]),
            }
        )
        # Get Extra Data
        match eigenval.data["ISPIN"]:
            case 1:
                eigenval.extra_data["spin-polarized"] = False
            case 2:
                eigenval.extra_data["spin-polarized"] = True
            case _:
                raise Exception

        # 读取主要数据
        data = []
        n_loop = (
            eigenval.data["n_bands"] + 2
        )  # 每一组数据的行数 = k点行 + 能带行 + 空行
        for kpoint_index in range(eigenval.data["n_kpoints"]):
            kpoint_line_index = 7 + kpoint_index * n_loop
            kw_data = [float(_) for _ in lines[kpoint_line_index].split()]
            for band_index in range(eigenval.data["n_bands"]):
                band_line_index = (
                    kpoint_line_index + 1 + band_index
                )  # 跳过 kpoint_line 行
                ew_data = [float(_) for _ in lines[band_line_index].split()]
                data.append(kw_data + ew_data)

        # 设置列名
        df = pd.DataFrame(
            data,
            columns=["k_a", "k_b", "k_c", "k_weight", "band_index"]
            + eigenval.data_columns[eigenval.extra_data["spin-polarized"]],
        )

        # 修改数据类型
        df["band_index"] = df["band_index"].astype(int)

        # 赋值
        eigenval.df = df

        # Return
        return eigenval

    @property
    def index_vbe(self) -> int:
        """
        Get the band index of the Valence Band Edge (VBE).
        (Start at 1)
        """
        match self.soc:
            case True:
                return self.data["n_electrons"]
            case False:
                return self.data["n_electrons"] / 2
            case _:
                raise ValueError(
                    "You must set the .soc attribute of your Eigenval object to `True` or `False` to get the index of band edge."
                )

    @property
    def index_cbe(self) -> int:
        """
        Get the band index of the Conduction Band Edge (VBE).
        (Start at 1)
        """
        return self.index_vbe + 1

    @property
    def energy_vbm(self) -> float:
        band = self.df[self.df["band_index"] == self.index_vbe]
        if self.extra_data["spin-polarized"]:
            return max(band["energy_1"].max(), band["energy_2"].max())
        else:
            return band["energy"].max()

    @property
    def energy_cbm(self) -> float:
        band = self.df[self.df["band_index"] == self.index_cbe]
        if self.extra_data["spin-polarized"]:
            return min(band["energy_1"].min(), band["energy_2"].min())
        else:
            return band["energy"].min()

    @property
    def energy_midgap(self) -> float:
        return (self.energy_vbm + self.energy_cbm) / 2

    def get_band(self, index: str | int):
        # Process
        if isinstance(index, str):
            match index.lower():
                case "vbe":
                    index = self.index_vbe
                case "cbe":
                    index = self.index_cbe
                case x if x.isdigit():
                    index = int(x)
                case _:
                    raise ValueError(f"Invalid band index: {index}")
        result = self.df[self.df["band_index"] == int(index)]
        result = result.reset_index(drop=True)
        # Error Handling
        if result.shape[0] == 0:
            raise IndexError(
                f"The energy band {index} was not found. Please check whether the band index or soc is set correctly."
            )
        # Return
        return result


if __name__ == "__main__":
    from tepkit import paths

    path = paths["test_files"] / "vasp_files/Bi2Te3-Band-3D-PBE/EIGENVAL"
    eigenval = Eigenval.from_file(path)
    print(eigenval.df)
    eigenval.soc = False
    print(eigenval.get_band("VBE"))
