from pathlib import Path
from typing import Literal, TypeAlias, Self

import numpy as np
import pandas as pd
from pandas import DataFrame

from tepkit.io.vasp import Outcar
from tepkit.types import number

_Tensor3x6RowIndex: TypeAlias = Literal["x", "y", "z"]
_Tensor3x6ColIndex: TypeAlias = Literal["xx", "yy", "zz", "xy", "xz", "yz"]
_VOIGT_NOTATION = ["xx", "yy", "zz", "yz", "zx", "xy"]


class PiezoelectricTensor:
    def __init__(
        self,
        matrix: list[list[number]] | np.ndarray,
        row_order: list[_Tensor3x6RowIndex],
        col_order: list[_Tensor3x6ColIndex],
        unit: str = "Unknown",
    ):
        matrix: np.ndarray = np.array(matrix).astype(float)
        if matrix.shape != (3, 6):
            raise ValueError("Matrix must be of shape (3, 6)")
        if len(row_order) != 3 or set(row_order) != {"x", "y", "z"}:
            raise ValueError(f"Invalid row order: {row_order}")
        col_order = [self.sort_index(col) for col in col_order]
        if len(col_order) != 6 or set(col_order) != {"xx", "yy", "zz", "xy", "xz", "yz"}:  # fmt: skip
            raise ValueError(f"Invalid column order: {col_order}")
        df = pd.DataFrame(
            matrix,
            index=np.array(row_order),
            columns=np.array(col_order),
        )
        self._df = df.reindex(
            index=["x", "y", "z"],
            columns=["xx", "yy", "zz", "yz", "xz", "xy"],
        )
        self.unit: str = unit

    @staticmethod
    def sort_index(index) -> _Tensor3x6ColIndex:
        mapping: dict[str, _Tensor3x6ColIndex] = {
            "xx": "xx",
            "yy": "yy",
            "zz": "zz",
            "xy": "xy",
            "yx": "xy",
            "xz": "xz",
            "zx": "xz",
            "yz": "yz",
            "zy": "yz",
        }
        return mapping[index]

    @property
    def df(self) -> DataFrame:
        return self._df.copy()

    @property
    def matrix(self) -> np.ndarray:
        return self._df.to_numpy()

    def reorder_direction(self, order) -> Self:
        if len(order) != 3 or set(order) != {"x", "y", "z"}:
            raise ValueError(f"Invalid direction order: {order}")
        row_mapping = {
            "x": order[0],
            "y": order[1],
            "z": order[2],
        }
        col_mapping = {
            "xx": order[0] + order[0],
            "yy": order[1] + order[1],
            "zz": order[2] + order[2],
            "yz": self.sort_index(order[1] + order[2]),
            "xz": self.sort_index(order[0] + order[2]),
            "xy": self.sort_index(order[0] + order[1]),
        }
        new_row_order = [row_mapping[i] for i in self._df.index]
        new_col_order = [col_mapping[i] for i in self._df.columns]
        self._df = self._df.reindex(
            index=new_row_order,
            columns=new_col_order,
        )
        return self


class PiezoelectricStressTensor(PiezoelectricTensor):
    @classmethod
    def from_vasp_outcar(
        cls,
        outcar: Outcar | Path,
        part: str = "total",
        cell_z=None,
    ):
        outcar: Outcar = Outcar.from_auto(outcar)
        result = outcar.get_piezoelectric_stress_tensors(cell_z=cell_z)
        df = result[part]
        return cls(
            matrix=df.to_numpy(),
            row_order=df.index,
            col_order=df.columns,
            unit=result["unit"],
        )


class PiezoelectricStrainTensor(PiezoelectricTensor):
    pass
