from typing import Callable

from tepkit.io import TableTextFile
from tepkit.io.indices import T3D_INDICES, EMPTY_INDEX
from tepkit.io.shengbte import TemperatureLengthFile, NticksLengthFile, SubdirFile


class KappaEtcMixin(TableTextFile):
    """
    Mixin class for kappa tensor files to apply effective thickness correction (ETC).
    """

    def __init__(self):
        super().__init__()
        self._etc_applied: bool = False
        """Whether the effective_thickness_correction() (ETC) has been applied."""

    def effective_thickness_correction(self, proportion: float) -> None:
        if not (0 < proportion <= 1):
            raise ValueError(
                "The thickness proportion (h_eff/h_cell) should between 0 to 1."
            )
        for direction in T3D_INDICES:
            self.df[("kappal", "W/(m*K)", direction)] /= proportion
        self._etc_applied = True

    @property
    def etc_applied(self) -> bool:
        """read-only property from outside."""
        return self._etc_applied


class KappaTensorVsT(TemperatureLengthFile, KappaEtcMixin):
    """
    For ShengBTE output files ``BTE.KappaTensorVsT_*`` .

    Supported Files
    ===============
    - BTE.KappaTensorVsT_CONV
    - BTE.KappaTensorVsT_RTA
    - BTE.KappaTensorVsT_sg
    """

    default_file_name = "BTE.KappaTensorVsT_CONV"
    column_indices = {
        "quantity": ["T"] + ["kappal"] * 9 + ["Step"],
        "unit": ["K"] + ["W/(m*K)"] * 9 + EMPTY_INDEX,
        "direction": EMPTY_INDEX + T3D_INDICES + EMPTY_INDEX,
    }

    def plot(self, ax, direction, color="blue"):
        df = self.df
        ax.plot(df["T"], df[("kappal", "W/(m*K)", direction)], color=color)
        ax.scatter(
            df["T"],
            df[("kappal", "W/(m*K)", direction)],
            zorder=100,
            color=color,
            edgecolor="#FFF",
            linewidth=0.8,
            marker="o",
            s=10,
        )


class CumulativeKappaTensor(NticksLengthFile, SubdirFile, KappaEtcMixin):
    """
    For ShengBTE output file ``BTE.cumulative_kappa_tensor`` .

    Supported Files
    ===============
    - BTE.cumulative_kappa_tensor
    """

    default_file_name = "BTE.cumulative_kappa_tensor"
    column_indices = {
        "quantity": ["MFP"] + ["kappal"] * 9,
        "unit": ["nm"] + ["W/(m*K)"] * 9,
        "direction": EMPTY_INDEX + T3D_INDICES,
    }

    def __init__(self):
        super().__init__()
        self.fit_func = {}
        self.x0 = {}

    def get_fit_func(self, direction) -> Callable:
        from scipy.optimize import curve_fit

        df = self.df
        y_max = max(df["kappal", "W/(m*K)", direction])

        def func(x, _x0):
            return y_max / (1 + _x0 / x)

        popt, *_ = curve_fit(
            func,
            df[("MFP", "nm", "-")],
            df[("kappal", "W/(m*K)", direction)],
        )
        x0 = popt[0]

        def func(x):
            return y_max / (1 + x0 / x)

        self.fit_func[direction] = func
        self.x0[direction] = x0

        return func

    def calculate_fitted_kappal(self, direction):
        fit_func = self.get_fit_func(direction)
        fitted_kappal = fit_func(self.df["MFP"])
        self.df[f"fit-kappal", "W/(m*K)", direction] = fitted_kappal
        return fitted_kappal

    def plot(self, ax, direction, fit=False, x0=False, color="blue"):
        df = self.df
        ax.plot(
            df["MFP"],
            df[("kappal", "W/(m*K)", direction)],
            color=color,
        )
        if fit:
            self.calculate_fitted_kappal(direction)
            ax.plot(
                df["MFP"],
                df[("fit-kappal", "W/(m*K)", direction)],
                color=color,
                linestyle="--",
                linewidth=0.6,
                alpha=0.8,
            )
            if x0:
                ax.scatter(
                    self.x0[direction],
                    self.fit_func[direction](self.x0[direction]),
                    zorder=100,
                    color=color,
                    edgecolor="#333",
                    linewidth=0.8,
                    marker="D",
                    s=10,
                )


class CumulativeKappaVsOmegaTensor(NticksLengthFile, SubdirFile, KappaEtcMixin):
    """
    For ShengBTE output file ``BTE.cumulative_kappaVsOmega_tensor`` .

    Supported Files
    ===============
    - BTE.cumulative_kappaVsOmega_tensor
    """

    default_file_name = "BTE.cumulative_kappaVsOmega_tensor"
    column_indices = {
        "quantity": ["Angular Frequency"] + ["kappal"] * 9,
        "unit": ["rad/ps"] + ["W/(m*K)"] * 9,
        "direction": EMPTY_INDEX + T3D_INDICES,
    }

    def plot(self, ax, direction, y_unit="rad/ps", color="blue"):
        df = self.df
        match y_unit:
            case "rad/ps":
                xs = df[("Angular Frequency", "rad/ps", "-")]
            case "THz":
                import math

                xs = df[("Angular Frequency", "rad/ps", "-")] / (2 * math.pi)
            case _:
                raise ValueError(f"Unsupported y_unit: {y_unit}")
        ys = df[("kappal", "W/(m*K)", direction)]
        ax.plot(
            xs,
            ys,
            color=color,
        )
