from tepkit.io.indices import V3D_INDICES
from tepkit.io.shengbte import (
    OmegaLengthFile,
    OmegaShapedFile,
    OmegaParalleledFile,
    SubdirFile,
)


class Omega(OmegaShapedFile):
    """
    For ShengBTE output file ``BTE.omega`` (Angular frequency).

    Table Strcture
    ==============

    .. list-table::
       :widths: 10 10 10 10
       :header-rows: 3
       :stub-columns: 1

       * - Quantity
         - Angular Frequency
         - —
         - ...
       * - Unit
         - rad/ps
         - —
         - ...
       * - Phonon Band Index
         - 1
         - 2
         - ...
       * - *q* point 0
         - *float*
         - *float*
         - ...
       * - ...
         - ...
         - ...
         - ...

    Supported Files
    ==================================
    - ``BTE.omega``

    """

    default_file_name = "BTE.omega"
    column_indices = {}

    def get_values(self, unit="rad/ps"):
        match unit:
            case "rad/ps":
                return self.df.values
            case "THz":
                import math

                return self.df.values / (2 * math.pi)
            case _:
                raise ValueError(f"Unsupported unit: {unit}")

    def plot_with(self, ax, y_table, x_unit="rad/ps", colors=None, group="111n"):
        x_table = self.get_values(unit=x_unit)
        modes = x_table.shape[1]
        match group.lower():
            case "ao":
                colors = [colors[0] for _ in range(3)] + [
                    colors[1] for _ in range(modes - 3)
                ]
                print(colors)
                labels = [""] * modes
                labels[0] = "Acoustic"
                labels[3] = "Optical"
            case "ztlo":
                colors = colors[:3] + [colors[3] for _ in range(modes - 3)]
                labels = ["ZA", "TA", "LA", "Optical"] + ["" for _ in range(modes - 4)]
            case "each":
                colors = colors
                labels = [f"Mode-{i}" for i in range(modes)]
            case _:
                raise ValueError(f"Unsupported group: {group}")
        for i in range(x_table.shape[1]):
            color = colors[i % len(colors)]
            ax.scatter(
                x_table[:, i],
                y_table[:, i],
                label=labels[i],
                s=2,
                # marker=marker,
                facecolors="None",
                edgecolors=color,
                linewidths=0.6,
                alpha=0.7,
                zorder=(modes - i) * 0.1,
            )


class V(OmegaLengthFile):
    """
    For ShengBTE output file ``BTE.v`` (Group velocity).

    Table Strcture
    ==============

    .. list-table::
       :widths: 10 10 10 10
       :header-rows: 3
       :stub-columns: 1

       * - Quantity
         - Group Velocity
         - —
         - —
       * - Unit
         - km/s
         - —
         - —
       * - Direction
         - x
         - y
         - z
       * - Line 0
         - *float*
         - *float*
         - *float*
       * - ...
         - ...
         - ...
         - ...

    Supported Files
    ===============
    - ``BTE.v``

    """

    default_file_name = "BTE.v"
    column_indices = {
        "quantity": ["velocity"] * 3,
        "unit": ["km/s"] * 3,
        "direction": V3D_INDICES,
    }

    def __init__(self, omega: Omega = None):
        super().__init__()
        self.omega = omega

    def calculate_speed(self):
        """
        增加 ("Frequency", "THz") 列
        """
        df = self.df
        vx = df[("velocity", "km/s", "x")]
        vy = df[("velocity", "km/s", "y")]
        vz = df[("velocity", "km/s", "z")]
        speed = (vx**2 + vy**2 + vz**2) ** 0.5
        self.df[("speed", "km/s", "-")] = speed
        return speed

    def plot(self, ax, direction, x_unit="rad/ps", colors=None, group="111n"):
        if self.omega is None:
            raise ValueError("omega is not set")
        x_table = self.omega.get_values(unit=x_unit)
        if direction == "speed":
            ys = self.calculate_speed()
        else:
            ys = self.df[("velocity", "km/s", direction)]
        y_table = ys.values.squeeze().reshape(x_table.shape, order="F")
        self.omega.plot_with(ax, y_table, x_unit=x_unit, colors=colors, group=group)


class W(OmegaParalleledFile, SubdirFile):
    """
    For ShengBTE output files ``BTE.w`` and ``BTE.w_*`` (Scattering rate).

    Table Strcture
    ==============

    .. list-table::
       :widths: 10 10 10
       :header-rows: 2
       :stub-columns: 1

       * - Quantity
         - Angular Frequency
         - Scattering Rate
       * - Unit
         - rad/ps
         - 1/ps
       * - Line 0
         - *float*
         - *float*
       * - ...
         - ...
         - ...

    Supported Files
    ==================================

    Root-dir Files
    ----------------------------------
    - ``BTE.w_boundary``
    - ``BTE.w_isotopic``

    Temperature-dependent-subdir Files
    ----------------------------------
    - ``BTE.w``
    - ``BTE.w_anharmonic``
    - ``BTE.w_anharmonic_plus``
    - ``BTE.w_anharmonic_minus``
    - ``BTE.w_final``

    """

    default_file_name = "BTE.w_final"
    column_indices: dict = {
        "quantity": ["Angular Frequency"] + ["Gamma"],
        "unit": ["rad/ps"] + ["1/ps"],
    }

    def __init__(self, omega: Omega = None):
        super().__init__()
        self.omega = omega

    def plot(self, ax, direction, x_unit="rad/ps", colors=None, group="111n"):
        if self.omega is None:
            raise ValueError("omega is not set")
        x_table = self.omega.get_values(unit=x_unit)
        ys = self.df.iloc[:, 1]
        y_table = ys.values.squeeze().reshape(x_table.shape, order="F")
        self.omega.plot_with(ax, y_table, x_unit=x_unit, colors=colors, group=group)


class Gruneisen(OmegaShapedFile):
    """
    For ShengBTE output file ``BTE.gruneisen`` (Grüneisen parameter).

    Supported Files
    ===============
    - BTE.gruneisen
    """

    default_file_name = "BTE.gruneisen"


class WP3(OmegaParalleledFile, SubdirFile):
    """
    For ShengBTE output files ``BTE.WP3`` and ``BTE.WP3_*`` \
    (Three-phonon weighted phase space).

    Supported Files
    ==================================

    Temperature-dependent-subdir Files
    ----------------------------------
    - ``BTE.WP3``
    - ``BTE.WP3_plus``
    - ``BTE.WP3_minus``
    """

    default_file_name = "BTE.WP3"
    column_indices = {
        "quantity": ["Angular Frequency"] + ["WP3"],
        "unit": ["rad/ps"] + ["ps^4 rad^-4"],
    }
