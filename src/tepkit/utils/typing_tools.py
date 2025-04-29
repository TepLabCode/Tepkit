from typing import TypeAlias, Any

try:
    from typing import Self, TypeVarTuple
except ImportError:  # python < 3.11
    from typing_extensions import Self, TypeVarTuple

Self: TypeAlias = Self

# ===== PathLike ===== #
import os

PathLike = str | os.PathLike

# ===== NumpyArray ===== #
import numpy as np
from typing import Literal, TypeVar

DataType = TypeVar("DataType")
NumpyArray: TypeAlias = np.ndarray[Any, np.dtype[DataType]]
NumpyArray2D: TypeAlias = np.ndarray[(Any, Any), np.dtype[DataType]]
NumpyArray3x3: TypeAlias = np.ndarray[(Literal[3], Literal[3]), np.dtype[DataType]]
NumpyArrayNx3: TypeAlias = np.ndarray[(Literal["N"], Literal[3]), np.dtype[DataType]]
NumpyArrayNxN: TypeAlias = np.ndarray[(Literal["N"], Literal["N"]), np.dtype[DataType]]

# import numpy.typing as npt
# from typing import Annotated
# Array3x3: TypeAlias = Annotated[npt.NDArray[DType], (Literal[3], Literal[3])]
# ArrayNx3: TypeAlias = Annotated[npt.NDArray[DType], (Literal["N"], Literal[3])]
# ArrayNxN: TypeAlias = Annotated[npt.NDArray[DType], (Literal["N"], Literal["N"])]

# ===== AutoValue ===== #
from dataclasses import dataclass


@dataclass
class AutoClass:
    repr_value: str = "Auto"
    str_value: str = "Auto"
    int_value: int = 0
    float_value: float = float(0)

    def __repr__(self):
        return str(self.repr_value)

    def __str__(self):
        return str(self.str_value)

    def __int__(self):
        return int(self.int_value)

    def __float__(self):
        return float(self.float_value)


AutoValue = AutoClass()
