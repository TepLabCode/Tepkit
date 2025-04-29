"""
BoltzTraP2
"""

import pandas as pd
import numpy as np

from tepkit.cli import logger
from tepkit.io import TableTextFile
from tepkit.io.indices import EMPTY_INDEX, T3D_INDICES
from tepkit.io.shengbte import KappaTensorVsT
from tepkit.utils.mpl_tools import Figure

fs_s = 1e-15  # 1 fs = 1e-15 s
Ang_cm = 1e-8  # 1 Ang = 1e-8 cm


class Condtens(TableTextFile):
    default_file_name = "interpolation.condtens"
    column_indices = {
        "quantity": ["Ef", "T", "N"] + ["sigma/tau"] * 9 + ["S"] * 9 + ["kappae/tau"] * 9,
        "unit": ["Ry", "K", "e/uc"] + ["S/(m*s)"] * 9 + ["V/K"] * 9 + ["W/(m*K*s)"] * 9,
        "direction": EMPTY_INDEX * 3 + T3D_INDICES * 3,
    }  # fmt: skip
    default_from_file_config = {
        "sep": r"\s+",
        "header": None,
        "skiprows": 1,
        "dtype": {1: float},
    }
    # Plot Settings
    label_texts = {
        # Quantity
        "Ef": R"E_\text{f}",
        "sigma/tau": R"\sigma / \tau",
        "kappae/tau": R"\kappa_\text{e} / \tau",
        "sigma": R"\sigma",
        "kappae": R"\kappa_\text{e}",
        "rho": R"\rho",
        "PF": R"\text{PF}",
        "m_eff": R"m_\text{eff}",
        # Unit
        "S/(m*s)": R"S/(m·s)",
        "W/(m*K*s)": R"W/(m·K·s)",
        "W/(m*K)": R"W/(m·K)",
        "cm^{-1}": R"cm${}^{-1}$",
        "cm^{-2}": R"cm${}^{-2}$",
        "cm^{-3}": R"cm${}^{-3}$",
        "W/(m*K^2)": R"W/(m·K${}^2$)",
        "m_e": R"$m_\text{e}$",
    }
    """You can change it to determine how to display the axis label."""

    def __init__(self):
        super().__init__()
        self.column_indices_dict = {
            "Ef": ("Ef", "Ry", "-"),
            "T": ("T", "K", "-"),
            "N": ("N", "e/uc", "-"),
            "sigma/tau": ("sigma/tau", "S/(m*s)", None),
            "S": ("S", "V/K", None),
            "kappae/tau": ("kappae/tau", "W/(m*K*s)", None),
        }
        self._etc_applied: bool = False
        """Whether the effective_thickness_correction() (ETC) has been applied."""
        self._multiply_time: bool = False

    @property
    def _index(self):
        """
        The shortname of self.column_indices_dict.
        """
        return self.column_indices_dict

    def get_index(
        self,
        quantity: str,
        direction: str = None,
        unit: str = None,
    ):
        if direction in ["x", "y", "z"]:
            direction *= 2
        return (
            self.column_indices_dict[quantity][0],
            unit or self.column_indices_dict[quantity][1],
            direction or self.column_indices_dict[quantity][2],
        )

    def get_ts(self, df=None) -> list[int]:
        """temperatures"""
        if df is None:
            df = self.df
        index_t = self._index["T"]
        ts = list(set(df[index_t]))
        ts.sort(key=lambda d: int(d))
        return ts

    def get_carrier_type_conditions(self, df=None):
        if df is None:
            df = self.df
        condition_hole = df[self._index["N"]] >= 0
        condition_elec = df[self._index["N"]] <= 0
        return {
            "h": condition_hole,
            "e": condition_elec,
        }

    def effective_thickness_correction(self, proportion: float) -> None:
        if self._multiply_time is True:
            raise ValueError(
                "Effective thickness correction must be done before multiply_relaxation_time()."
            )
        if not proportion > 0 and proportion <= 1:
            raise ValueError(
                "The thickness proportion (h_eff/h_cell) should between 0 to 1."
            )
        for direction in T3D_INDICES:
            self.df[("sigma/tau", "S/(m*s)", direction)] /= proportion
            self.df[("kappae/tau", "W/(m*K*s)", direction)] /= proportion
        self._etc_applied = True

    def add_relaxation_time(
        self,
        value: float,
        value_t: float,
        direction: str,
        carrier_type: str,
        with_inverse_proportion: bool = False,
    ) -> None:
        """
        Add relaxation time (tau) to the dataframe.

        :param value: the relaxation time value in fs.
        :param value_t: the temperature of the relaxation time.
        :param direction: the direction of the relaxation time.
        :param carrier_type: the carrier type of the relaxation time. ["h", "e"]
        :param with_inverse_proportion: if True, it will assume that τ ∝ 1/T,
                                        the relaxation time at all temperatures will be autofilled by
                                        value * value_t / target_t.

        Example
        =======

        .. code-block:: python

            for t in obj.get_ts():
                obj.add_relaxation_time(
                    value=time_at_300k * 300 / t,
                    t=t,
                    direction="x",
                    carrier_type="h",
                )

        """
        if direction in ["x", "y", "z"]:
            direction *= 2
        df = self.df
        condition_type = self.get_carrier_type_conditions(df)[carrier_type]
        index_tau = ("tau", "fs", direction)
        if with_inverse_proportion:
            for t in self.get_ts():
                condition_t = df[self._index["T"]] == t
                self.df.loc[condition_t & condition_type, index_tau] = (
                    value * value_t / t
                )
        else:
            condition_t = df[self._index["T"]] == value_t
            self.df.loc[condition_t & condition_type, index_tau] = value

    def add_kappal(
        self,
        value: float,
        value_t: float,
        direction: str,
        with_inverse_proportion: bool = False,
        etc_applied: bool = False,
    ) -> None:
        """
        Add lattice thermal conductivity (kappal) to the dataframe.

        :param value: the kappal value in W/(m·K).
        :param value_t: the temperature of the kappal.
        :param direction: the direction of the kappal.
        :param with_inverse_proportion: if True, it will assume that κ_l ∝ 1/T,
                                        the kappal at all temperatures will be autofilled by
                                        value * value_t / target_t.
        :param etc_applied: if True, it means that the effective thickness correction
                                        has been done to the input kappal.
        :return:
        """
        if etc_applied != self._etc_applied:
            raise ValueError(
                "The state of effective thickness correction of kappa_l and kappa_e & sigma must be consistent."
            )
        if direction in ["x", "y", "z"]:
            direction *= 2
        df = self.df
        index_kappal = ("kappal", "W/(m*K)", direction)
        if with_inverse_proportion:
            for t in self.get_ts():
                condition_t = df[self._index["T"]] == t
                self.df.loc[condition_t, index_kappal] = value * value_t / t
        else:
            condition_t = df[self._index["T"]] == value_t
            self.df.loc[condition_t, index_kappal] = value
        self.column_indices_dict["kappal"] = ("kappal", "W/(m*K)", None)

    def add_kappal_from_shengbte(
        self,
        kappal: KappaTensorVsT,
    ) -> None:
        df = kappal.df
        col_t = df.iloc[:, 0]
        for t in list(col_t):
            if t not in self.get_ts():
                continue
            for d in T3D_INDICES:
                self.add_kappal(
                    value=df.loc[col_t == t, ("kappal", "W/(m*K)", d)].values[0],
                    value_t=t,
                    direction=d,
                    with_inverse_proportion=False,
                    etc_applied=kappal.etc_applied,
                )
        pass

    def calculate_carrier_density(
        self,
        lattice,
        *,
        dimension: int,
        abs_density: bool = True,
    ):
        """

        :param lattice: Unit: Angstrom.
        :param dimension:
        :param abs_density:
        :return:
        """
        df = self.df
        number = df[("N", "e/uc", "-")]
        lattice = np.array(lattice)
        match dimension:
            case 1:
                length = abs(float(lattice[0, 0]))
                value = number / (length * Ang_cm)
                unit = "cm^{-1}"
            case 2:
                area = abs(float(np.linalg.det(lattice[:2, :2])))
                value = number / (area * Ang_cm**2)
                unit = "cm^{-2}"
            case 3:
                volume = abs(float(np.linalg.det(lattice)))
                value = number / (volume * Ang_cm**3)
                unit = "cm^{-3}"
            case _:
                raise ValueError(f"Invalid dimension: {dimension}")
        if abs_density:
            value = abs(value)
        df[("rho", unit, "")] = value
        self.column_indices_dict["rho"] = ("rho", unit, "")

    def calculate_average_effective_mass(
        self,
        mass_unit: str,
        *,
        volume: float,
        _absolute: bool = True,
    ):
        """
        Calculate the DOS average effective mass.
        Add the columns ("m_eff", mass_unit, direction) to the self.df.

        Ref:
        - Hautier, G., et al. (2014). Chemistry of Materials, 26(19), 5447-5458.
        - Hautier, G., et al. (2013). Nature Communications, 4, 2292.

        :param mass_unit: Should be "kg", "g", or "m_e".
        :param volume: The volume of the cell. (Unit: m^3)
        :param _absolute: If False, the sign of the effective mass will be consistent with the `N`,
                          which means negative for electrons, and positive for holes.
        """
        if self._etc_applied:
            logger.warning(
                "The effective thickness correction has already been applied.\n"
                "Thus, the volume of `calculate_average_effective_mass()` should also be effective volume "
                "(= cell_volume * effective_thickness_proportion)\n"
                "We recommend to use `calculate_average_effective_mass()` with cell volume "
                "before `effective_thickness_correction()` to avoid this warning."
            )
        from scipy import constants

        df = self.df
        sigma_tau_indices = [("sigma/tau", "S/(m*s)", d) for d in T3D_INDICES]
        sigma_tau_tensor = df[sigma_tau_indices].values.reshape(-1, 3, 3)
        inv_sigma_tau_tensor = []
        for i in range(len(sigma_tau_tensor)):
            try:
                inv_i = np.linalg.inv(sigma_tau_tensor[i])
            except np.linalg.LinAlgError:
                inv_i = np.zeros((3, 3))
            inv_sigma_tau_tensor.append(inv_i)
        carrier_density = np.array(df[("N", "e/uc", "-")].values) / volume
        eff_mass = (
            inv_sigma_tau_tensor * carrier_density.reshape(-1, 1, 1) * constants.e**2
        )
        match mass_unit:
            case "kg":
                pass
            case "g":
                eff_mass = eff_mass * 1000
            case "m_e":
                eff_mass = eff_mass / constants.m_e
            case _:
                raise ValueError(
                    f"Invalid mass unit: {mass_unit}, should be 'kg', 'g', or 'm_e'."
                )
        if _absolute:
            eff_mass = np.abs(eff_mass)
        # Add data to self.df
        for i, direction_i in enumerate(["x", "y", "z"]):
            for j, direction_j in enumerate(["x", "y", "z"]):
                index = ("m_eff", mass_unit, direction_i + direction_j)
                self.df[index] = eff_mass[:, i, j]
        self.column_indices_dict["m_eff"] = ("m_eff", mass_unit, None)

    def multiply_relaxation_time(self, drop_tau: bool = False, get_pf: float = True):
        """
        Get multiply the relaxation time to the sigma and kappae.

        :param drop_tau: If True, it will drop the tau, sigma/tau, and kappae/tau columns.
        :param get_pf: If True, it will also calculate the power factor.
        """
        index_df = pd.DataFrame(list(self.df.columns))
        if "tau" not in list(index_df[0]):
            raise ValueError(
                "You must do add_relaxation_time() before multiply_relaxation_time()."
            )
        df = self.df
        self._multiply_time = True
        directions = list(index_df[index_df[0] == "tau"][2])
        for d in directions:
            if self.df[("tau", "fs", d)].isna().sum() > 0:
                logger.warning(
                    f"The {d} relaxation time is not all filled with values. "
                    + "The result may contain NaN or empty values."
                )
            df[("sigma", "S/m", d)] = df[("sigma/tau", "S/(m*s)", d)] * (
                df[("tau", "fs", d)] * fs_s
            )
            df[("kappae", "W/(m*K)", d)] = df[("kappae/tau", "W/(m*K*s)", d)] * (
                df[("tau", "fs", d)] * fs_s
            )
        self.column_indices_dict.update(
            {
                "tau": ("tau", "fs", None),
                "sigma": ("sigma", "S/m", None),
                "kappae": ("kappae", "W/(m*K)", None),
            }
        )
        if drop_tau:
            df.drop(columns=["tau", "sigma/tau", "kappae/tau"], level=0, inplace=True)
            self.column_indices_dict.pop("tau")
            self.column_indices_dict.pop("sigma/tau")
            self.column_indices_dict.pop("kappae/tau")
        if get_pf:
            for d in directions:
                df[("PF", "W/(m*K^2)", d)] = (
                    df[("S", "V/K", d)] * df[("S", "V/K", d)] * df[("sigma", "S/m", d)]
                )
            self.column_indices_dict["PF"] = ("PF", "W/(m*K^2)", None)

    def calculate_zt(self):
        index_df = pd.DataFrame(list(self.df.columns))
        if "kappal" not in list(index_df[0]):
            raise ValueError("You must do add_kappal() before get_zt().")
        df = self.df
        directions1 = set(index_df[index_df[0] == "kappal"][2])
        directions2 = set(index_df[index_df[0] == "kappae"][2])
        directions = sorted(directions1 & directions2)
        for d in directions:
            if self.df[("kappal", "W/(m*K)", d)].isna().sum() > 0:
                logger.warning(
                    f"The {d} kappal is not all filled with values. "
                    + "The result may contain NaN or empty values."
                )
            # zT = (S^2 * σ * T) / (κ_e + κ_l)
            df[("zT", "", d)] = (
                df[("S", "V/K", d)]
                * df[("S", "V/K", d)]
                * df[("sigma", "S/m", d)]
                * df[("T", "K", "-")]
                / (df[("kappae", "W/(m*K)", d)] + df[("kappal", "W/(m*K)", d)])
            )
        self.column_indices_dict["zT"] = ("zT", "", None)

    def plot(
        self,
        ax,
        x: str,
        y: str,
        t: float,
        x_unit: str = None,
        y_unit: str = None,
        x_direction: str = None,
        y_direction: str = None,
        carrier_type: str = None,
        **plot_kwargs,
    ):
        if ax is None:
            figure = Figure(height=0.7)
            ax = figure.ax
        if x.startswith("log-"):
            ax.set_xscale("log")
            x = x[4:]
        if y.startswith("log-"):
            ax.set_yscale("log")
            y = y[4:]
        x_index = list(self.column_indices_dict[x])
        y_index = list(self.column_indices_dict[y])
        if x_unit:
            x_index[1] = x_unit
        if y_unit:
            y_index[1] = y_unit
        if x_direction:
            if x_direction in ["x", "y", "z"]:
                x_direction *= 2
            x_index[2] = x_direction
        if y_direction:
            if y_direction in ["x", "y", "z"]:
                y_direction *= 2
            y_index[2] = y_direction

        df = self.df
        df = df[df[self._index["T"]] == t]
        match carrier_type:
            case "h":
                df = df[df[self._index["N"]] > 0]
            case "e":
                df = df[df[self._index["N"]] < 0]
            case None:
                pass
            case _:
                raise ValueError(
                    f"Invalid carrier type: {carrier_type}, should be 'h', 'e', or None."
                )
        xs = df[tuple(x_index)]
        ys = df[tuple(y_index)]
        result = ax.plot(xs, ys, **plot_kwargs)
        ax.set_xlabel(
            f"${self.get_label_text(x_index[0])}$ ({self.get_label_text(x_index[1])})".replace(
                " ()", ""
            )
        )
        ax.set_ylabel(
            f"${self.get_label_text(y_index[0])}$ ({self.get_label_text(y_index[1])})".replace(
                " ()", ""
            )
        )
        return result

    def get_label_text(self, text: str) -> str:
        return self.label_texts.get(text, text)


if __name__ == "__main__":
    pass
