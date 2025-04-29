from pathlib import Path
from pandas import DataFrame
from tepkit.io import File, TableTextFile
from tepkit.utils.typing_tools import PathLike, Self

__all__ = [
    "SubdirFile",
    "OmegaShapedFile",
    "OmegaLengthFile",
    "OmegaParalleledFile",
    "NticksLengthFile",
    "TemperatureLengthFile",
]


class SubdirFile(File):
    """
    ShengBTE 温度子文件夹中文件的文件类。
    """

    t: int = None
    """ The temperature (K) of the subdir. """

    @classmethod
    def from_dir(
        cls,
        path: PathLike = None,
        file_name: str = None,
        t: int = None,  # @override: New Argument
    ) -> Self:
        """
        @override File.from_dir()
        Add `t` (temperature) argument to specify the subdir f\"T{t}K\".
        """
        if t is not None:
            path = Path(path) / f"T{t}K"
        obj = super().from_dir(path, file_name)
        obj.t = t
        return obj


class OmegaShapedFile(TableTextFile):
    """
    与 BTE.omega 的数据形状相同的数据文件。
    @shape: (n_qpoints, n_modes)
    ---
    Supported Files:
    - ``BTE.gruneisen``
    - ``BTE.omega``
    - ``BTE.P3*``
    - ``BTE.P4*``
    """

    def __init__(self, omega=None):
        super().__init__()
        self.omega = omega

    def set_mode_names(self, names=None):
        df = self.df
        df.columns = df.columns.map(str)
        if names is None:
            df.columns.values[0:3] = ["ZA", "TA", "LA"]
            df.columns.values[3:] = [
                f"Optical-{i}" for i in range(1, len(df.columns.values[3:]) + 1)
            ]
        elif len(names) != len(self.df.columns.values):
            raise ValueError(
                "Length of names should be equal to the number of columns."
            )
        else:
            df.columns.values = names
        self.df = df

    def plot(self, ax, x_unit="rad/ps", colors=None, group="111n"):
        if self.omega is None:
            raise ValueError("omega is not set")
        y_table = self.df.values
        self.omega.plot_with(ax, y_table, x_unit=x_unit, colors=colors, group=group)


class OmegaLengthFile(TableTextFile):
    """
    与 频率 行数相同的数据文件。
    @shape: (n_qpoints * n_modes, [Any])
    ---
    Supported Files:
    - ``BTE.v*``
    """

    column_indices = {
        "quantity": ["Angular Frequency"],
        "unit": ["rad/ps"],
    }
    column_indices_autofill = {"prefix": "Column-", "start": 0}


class OmegaParalleledFile(TableTextFile):
    """
    由 频率 和 数值 两列数据组成的数据文件。
    @shape: (n_qpoints * n_modes, 2)
    ---
    Supported Files:
    - ``BTE.w*``
    - ``T*K/``

        - ``BTE.WP3*``
        - ``BTE.WP4*``
        - ``BTE.w*``
    """

    column_indices = {
        "quantity": ["Angular Frequency"] + ["Value"],
        "unit": ["rad/ps"] + ["-"],
    }

    def reshape_to(self, shape):
        y = self.df.iloc[:, 1]
        return DataFrame(y.values.reshape(shape, order="F"))


class NticksLengthFile(TableTextFile):
    """
    由 nticks (default=100) 决定行数的数据文件。
    @shape: (n_qpoints * n_modes, [Any])
    ---
    Supported Files:
    - BTE.dos
    - BTE.pdos
    - ``T*K``/

        - ``BTE.cumulative_kappa*``
    """

    pass


class TemperatureLengthFile(TableTextFile):
    """
    由 Ts 决定行数的数据文件, 且第一列为温度。
    @shape: (Ts, T + [Any])
    ---
    Supported Files:
    - BTE.*VsT*
    """

    default_from_file_config = {
        "sep": r"\s+",
        "header": None,
        "skiprows": 0,
    }
    column_indices = {
        "quantity": ["Temperature"],
        "unit": ["K"],
    }
    column_indices_autofill = {"prefix": "Column-", "start": 0}

    def __init__(self):
        super().__init__()
