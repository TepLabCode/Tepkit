import tomllib
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from tepkit.cli import InvalidArgumentError, logger
from tepkit.core.geometry import rotate_matrix_2d
from tepkit.core.high_symmetry_points import HighSymmetryPoints2D
from tepkit.core.structure import abc_to_xyz
from tepkit.core.symmetry import BravaisLattice2D
from tepkit.io.vasp import Eigenval, Outcar, Poscar
from tepkit.utils.mpl_tools import Figure
from tepkit.utils.mpl_tools.color_tools import get_colormap
from tepkit.utils.mpl_tools.formatters import get_decimal_formatter
from tepkit.utils.mpl_tools.plotters import BrillouinZone2DPlotter, Plotter
from tepkit.utils.mpl_tools.ticker_tools import set_axes_ticker_formatter


def _symmetrize(matrix, x, y, z, others=None):
    # Error Handling
    matrix = np.array(matrix)
    if matrix.shape != (3, 3):
        raise ValueError(
            f"the shape of the matrix must be (3, 3), but not {matrix.shape}"
        )
    if not ((len(x) == len(y)) and (len(x) == len(z))):
        raise ValueError("x, y, z must have the same length")
    if others is None:
        values = np.empty((0, len(x)))
    else:
        values = others

    # Process
    xyz = np.array((x, y, z))
    m_xyz = np.dot(matrix, xyz)
    result = np.hstack(
        (
            np.vstack((xyz, values)),
            np.vstack((m_xyz, values)),
        )
    )
    result = np.unique(result, axis=1)
    if others is None:
        return result[0], result[1], result[2]
    else:
        return result[0], result[1], result[2], result[3]


def _fully_symmetrize(matrixs, x, y, z, others=None):
    result = (x, y, z, others)
    for matrix in matrixs:
        result = _symmetrize(matrix, *result)
    return result


class _BandContourPlotter(Plotter):
    def __init__(self, x, y, e, cmap="tepkit_rainbow_ex"):
        super().__init__()
        self.config = {
            "colorbar_settings": {
                "colorbar_kwargs": {
                    "pad": 0.07,
                    "height": 0.88,
                    "width": 0.9,
                },
                "axhline_kwargs": {
                    "color": "k",
                    "linestyle": "--",
                    "lw": 0.3,
                },
                "title_text_kwargs": {
                    "x": -0.5,
                    "y": 0.02,
                    "s": "Energy (eV)",
                    "ha": "right",
                    "va": "bottom",
                    "fontsize": 8,
                    "rotation": 90,
                },
                "max_text_fontsize": 8,
                "min_text_fontsize": 8,
                "tick_text_fontsize": 10,
            },
            "legend_kwargs": {
                "border_width": 0.5,
                "fancybox": False,
                "edgecolor": "black",
                "handletextpad": 0.2,
                "handlelength": 0.7,
                "fontsize": 6,
                "borderpad": 0.4,
                "loc": "best",
            },
        }
        self._data_layer = None
        self._colormap = get_colormap(cmap)
        self._df = None

        self.x = x
        self.y = y
        self.e = e
        self.contour_levels = e.min() + np.linspace(0.03, 0.97, 7) * (e.max() - e.min())

    @staticmethod
    def set_axis(ax, show: bool):
        if show:
            ax.axis("on")
            ax.set_xlabel("$k_x$")
            ax.set_ylabel("$k_y$")
            plt.subplots_adjust(left=0.18, right=0.96, top=0.93, bottom=0.18)
        else:
            ax.axis("off")
            plt.subplots_adjust(left=0.04, right=0.96, top=0.93, bottom=0.07)

    def plot_tricontour(self, ax, *, colors, linewidths):
        """
        Plot the tricontour of the data.
        绘制二维等高线。
        """
        return ax.tricontour(
            self.x, self.y, self.e,
            linewidths=linewidths,
            colors=colors,
            linestyles="dashed",
            levels=self.contour_levels,
        )  # fmt: skip

    def plot_tricontourf(self, ax, *, cmap=None, levels=256):
        """
        Plot the tricontourf of the data.
        绘制二维热力图。
        """
        data_layer = ax.tricontourf(
            self.x, self.y, self.e,
            cmap=cmap or self._colormap,
            levels=levels,
        )  # fmt:skip
        self._data_layer = data_layer
        return data_layer

    def plot_tripcolor(self, ax):
        """
        Plot the tripcolor of the data.
        绘制二维三角面图。
        """
        data_layer = ax.tripcolor(
            self.x, self.y, self.e,
            cmap=self._colormap,
        )  # fmt:skip
        self._data_layer = data_layer
        return data_layer

    def plot_colorbar(self, figure):
        """
        Plot the colorbar of the figure.
        绘制颜色条。
        """
        # Create Colorbar
        colorbar_kwargs = self.config["colorbar_settings"]["colorbar_kwargs"]
        cbar = figure.add_colorbar(self._data_layer, **colorbar_kwargs)
        # Tick / 刻度
        cbar.set_ticks(self.contour_levels)
        cbar.ax.tick_params(
            labelsize=self.config["colorbar_settings"]["tick_text_fontsize"], length=0
        )
        # Set Colorbar Formatter
        max_fmtr = get_decimal_formatter(3)
        tickle_fmtr = get_decimal_formatter(2)
        set_axes_ticker_formatter(cbar.ax, "y", "func", tickle_fmtr)
        # Max / 最大值
        cbar.ax.text(
            0.5,
            1.02,
            max_fmtr(self.e.max()),
            ha="center",
            va="baseline",
            fontsize=self.config["colorbar_settings"]["max_text_fontsize"],
            transform=cbar.ax.transAxes,
        )
        # Min / 最小值
        cbar.ax.text(
            0.5,
            -0.02,
            max_fmtr(self.e.min()),
            ha="center",
            va="top",
            fontsize=self.config["colorbar_settings"]["min_text_fontsize"],
            transform=cbar.ax.transAxes,
        )
        # Title / 标题
        title_text_kwargs = self.config["colorbar_settings"]["title_text_kwargs"]
        title_text_kwargs["transform"] = cbar.ax.transAxes
        cbar.ax.text(**title_text_kwargs)
        # Tick Mark / 刻度线
        axhline_kwargs: dict = self.config["colorbar_settings"]["axhline_kwargs"]
        axhline_colors: list = axhline_kwargs.pop("colors", None)
        if axhline_colors:
            axhline_kwargs.pop("color")
            for level, color in zip(self.contour_levels, axhline_colors):
                cbar.ax.axhline(level, color=color, **axhline_kwargs)
        else:
            for level in self.contour_levels:
                cbar.ax.axhline(level, **axhline_kwargs)

    def plot_input_data_points(self, ax, df):
        points_weighted = df[df.k_weight != 0]
        points_zero_weighted = df[df.k_weight == 0]
        # 有权重的 SCF 点
        ax.plot(
            points_weighted.k_x,
            points_weighted.k_y,
            markerfacecolor="lightgrey",
            color="#444444",
            marker="o",
            markersize=1.5,
            linestyle="None",
            markeredgewidth=0.3,
        )
        # 无权重的能带点
        ax.plot(
            points_zero_weighted.k_x,
            points_zero_weighted.k_y,
            markerfacecolor="lightblue",
            color="#666666",
            marker="o",
            markersize=0.8,
            linestyle="None",
            markeredgewidth=0.1,
        )

    def plot_all_data_points(self, ax, x, y):
        ax.plot(
            x,
            y,
            markerfacecolor="#EEE",
            color="#666666",
            marker="o",
            markersize=1,
            linestyle="None",
            markeredgewidth=0.2,
        )

    def plot_legend(self, figure):
        legend_kwargs = self.config["legend_kwargs"]
        figure.add_legend(**legend_kwargs)


_presets = {
    "none": {},
    # Automatically recognize symmetry
    "auto": {},
    # Only consider the inversion, work well with Tepkit generated kpoints.
    "basic": {
        "xyz_matrices": {
            "inversion": [[-1, 0, 0], [0, -1, 0], [0, 0, -1]],
        },
    },
    # Oblique
    "mp": {
        "xyz_matrices": {
            "inversion": [[-1, 0, 0], [0, -1, 0], [0, 0, -1]],
        },
    },
    # Rectangular
    "op": {
        "xyz_matrices": {
            "mirror (x-axis)": [[-1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "mirror (y-axis)": [[1, 0, 0], [0, -1, 0], [0, 0, 1]],
        },
    },
    # Centered Rectangular
    "oc": {
        "abc_matrices": {
            "mirror (b2=b1)": [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        },
        "xyz_matrices": {
            "inversion": [[-1, 0, 0], [0, -1, 0], [0, 0, -1]],
        },
    },
    # Square
    "tp": {
        "xyz_matrices": {
            "rotate (1/4)": rotate_matrix_2d(90, to_3d=True),
            "mirror (x-axis)": [[-1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "mirror (y-axis)": [[1, 0, 0], [0, -1, 0], [0, 0, 1]],
        },
    },
    # Hexagonal
    "hp": {
        "xyz_matrices": {
            "rotate (1/6)": rotate_matrix_2d(60, to_3d=True),
            "rotate (2/6)": rotate_matrix_2d(120, to_3d=True),
            "rotate (3/6)": rotate_matrix_2d(180, to_3d=True),
            "rotate (4/6)": rotate_matrix_2d(240, to_3d=True),
            "rotate (5/6)": rotate_matrix_2d(300, to_3d=True),
            "mirror (y-axis)": [[1, 0, 0], [0, -1, 0], [0, 0, 1]],
        },
    },
}


def _get_file_obj(cls, arg, fallback_dir):
    if isinstance(arg, cls):
        return arg
    elif arg is not None:
        return cls.from_file(arg)
    else:
        return cls.from_dir(fallback_dir)


def _strbool(s: str) -> bool:
    if not isinstance(s, str):
        raise TypeError(f"Invalid option: {s}, should be string 'on' or 'off'.")
    match s.lower():
        case "on":
            return True
        case "off":
            return False
        case _:
            raise InvalidArgumentError(f"Invalid option: {s}, should be 'on' or 'off'.")


def band_contour(
    preset: str,
    # File Settings / 文件设置
    data_dir: Path = "./",
    eigenval: Path = None,  # Path | Eigenval | None
    poscar: Path = None,  # Path | Poscar | None
    outcar: Path = None,  # Path | Outcar | None
    save_dir: Path = "./",
    save_prefix: str = "tepkit.band_contour",
    # Data Selecting / 数据选择
    soc: bool = False,
    index: str = "edges",
    spin: str = "auto",
    # Data Processing / 数据处理
    ref: str = "0",
    sym_prec: float = 1e-5,
    # Plot Settings / 绘图设置
    plot_config: Path = None,
    plot_axis: str = "off",
    plot_arrow: str = "on",
    plot_boundary: str = "on",
    plot_path: str = "off",
    plot_cbar: str = "on",
    plot_legend: str = "on",
    plot_cline: str = "black",
    plot_point: str = "off",
    plot_bms: str = "all",
    map_engine: str = "tricontourf",
    colormap: str = "tepkit_rainbow_ex",
):
    R"""
    Plot the contour map of the electronic band structure.
    (on the xy-plane of the material's Brillouin zone)

    Suggested Steps:
    1. use `-p none --point input` to cheak your data.
    2. use `-p auto --path on --point all` to cheak the symmetry operations.
    3. use `-p auto --path on --arrow off` and your custom options to plot the final results.

    :param preset       : [green]( none / auto / basic / \[symmetry] )[/] The preset of structure symmetry. &
                          [green]symmetry = ( obl / rec / cen / squ / hex )[/]
    :param data_dir     : The directory of the input files.
    :param eigenval     : Override the path of the EIGENVAL file.
    :param poscar       : Override the path of the POSCAR file.
    :param outcar       : Override the path of the OUTCAR file. &
                          [bright_black](Only used when --ref is "outcar_fermi")[/bright_black]
    :param save_dir     : The directory to save the output figures.
    :param save_prefix  : The prefix name of the output figures.
    :param soc          : Used when the result is under SOC.
    :param index        : [green]( edges / vbe / cbe / \[int] )[/] The index of the band to plot.
    :param spin         : [green]( auto / up / down )[/]
    :param ref          : [green]( outcar_fermi / midgap / \[float(eV)] )[/] Thr reference of zero energy.
    :param sym_prec     : The precision to find the symmetry when `preset` is "auto".
    :param plot_config  : The path of the detailed config file for plotting.
    :param plot_axis    : [green]( off / on )[/] The axis of figure.
    :param plot_arrow   : [green]( off / on )[/] The base vectors of the reciprocal lattice.
    :param plot_boundary: [green]( off / on )[/] The boundary of the Brillouin zone.
    :param plot_path    : [green]( off / on )[/] The path of the high-symmetry points.
    :param plot_cbar    : [green]( off / on )[/] The colorbar of the contour map.
    :param plot_legend  : [green]( off / on )[/] The legend of the VBM/CBM point.
    :param plot_cline   : [green]( off / colorful / \[color] )[/] How to plot contour lines.
    :param plot_point   : [green]( off / input / all )[/] How to plot data points.
    :param plot_bms     : [green]( off / input / all )[/] How to plot VBM / CBM point.
    :param map_engine   : [green]( off / tricontourf / tripcolor )[/] How to plot the contour map.
    :param colormap     : The colormap of the contour map or colorful contour lines.

    :typer preset        flag: --preset, -p
    :typer soc           flag: --soc
    :typer plot_config   flag: --config
    :typer plot_axis     flag: --axis
    :typer plot_arrow    flag: --arrow
    :typer plot_boundary flag: --boundary
    :typer plot_path     flag: --path
    :typer plot_cbar     flag: --cbar
    :typer plot_legend   flag: --legend
    :typer plot_cline    flag: --cline
    :typer plot_point    flag: --point
    :typer plot_point    flag: --point
    :typer plot_bms      flag: --bms

    :typer preset      panel: Required
    :typer data_dir    panel: File Settings
    :typer eigenval    panel: File Settings
    :typer poscar      panel: File Settings
    :typer outcar      panel: File Settings
    :typer save_dir    panel: File Settings
    :typer save_prefix panel: File Settings
    :typer soc         panel: Data Selecting
    :typer index       panel: Data Selecting
    :typer spin        panel: Data Selecting
    :typer ref         panel: Data Processing
    :typer sym_prec    panel: Data Processing
    :typer plot_config   panel: Plot Settings
    :typer plot_axis     panel: Plot Settings
    :typer plot_arrow    panel: Plot Settings
    :typer plot_boundary panel: Plot Settings
    :typer plot_path     panel: Plot Settings
    :typer plot_cbar     panel: Plot Settings
    :typer plot_legend   panel: Plot Settings
    :typer plot_cline    panel: Plot Settings
    :typer plot_point    panel: Plot Settings
    :typer plot_bms      panel: Plot Settings
    :typer map_engine    panel: Plot Settings
    :typer colormap      panel: Plot Settings

    :typer plot_config hidden:
    """
    # Save Input Arguments / 保存输入参数
    args = locals()

    # Read EIGENVAL
    eigenval = _get_file_obj(Eigenval, eigenval, data_dir)
    eigenval.soc = soc
    args["eigenval"] = eigenval

    # Read POSCAR
    poscar = _get_file_obj(Poscar, poscar, data_dir)
    args["poscar"] = poscar

    # Process `index`
    index = index.lower()
    if index == "edges":
        # Recurs VBE and CBE / 递归 VBE 和 CBE
        # VBE
        logger.info("Start for VBE ...")
        args["index"] = "vbe"
        band_contour(**args)
        # CBE
        logger.info("Start for CBE ...")
        args["index"] = "cbe"
        band_contour(**args)
        # Return
        return

    # Get Data / 获取数据
    df = eigenval.get_band(index=index)

    # Process `spin`
    spin = spin.lower()
    if eigenval.extra_data["spin-polarized"] is True:
        match spin:
            case "auto":
                # Recurs up and down / 递归 up 和 down
                # Spin up
                logger.info("Start for spin up ...")
                args["spin"] = "up"
                band_contour(**args)
                # Spin down
                logger.info("Start for spin down ...")
                args["spin"] = "down"
                band_contour(**args)
                # Return
                return
            case "up":
                df["energy"] = df.energy_1
            case "down":
                df["energy"] = df.energy_2
            case _:
                raise InvalidArgumentError(f"Invalid spin: {spin}")
    else:
        if spin != "auto":
            raise InvalidArgumentError(
                "Invalid spin: {spin}, can only be 'auto' when the result is not spin-polarized."
            )

    # Process `ref`
    match ref.lower():
        case "outcar_fermi":
            outcar = _get_file_obj(Outcar, outcar, data_dir)
            ref_e = outcar.fermi_energy
        case "midgap":
            ref_e = eigenval.energy_midgap
        case _:
            ref_e = float(ref)
    df["energy"] = df["energy"] - ref_e

    # Process `preset`
    preset = preset.lower()
    bravais_lattice_2d = None
    match preset:
        case "none":
            pass
        case "basic":
            pass
        case "auto":
            bravais_lattice_2d = BravaisLattice2D.from_poscar(poscar, sym_prec=sym_prec)
            preset = bravais_lattice_2d.to_string("short")
        case _:
            bravais_lattice_2d = BravaisLattice2D.from_string(preset)
            preset = bravais_lattice_2d.to_string("short")
    preset = _presets[preset]

    # Data Symetrization / 数据对称化
    b_lattice = poscar.reciprocal_lattice
    df["k_x"], df["k_y"], df["k_z"] = abc_to_xyz(
        abc=np.column_stack((df.k_a, df.k_b, df.k_c)),
        lattice=b_lattice,
    ).T
    a, b, c, e = df.k_a, df.k_b, df.k_c, df.energy
    a, b, c, e = np.unique((a, b, c, e), axis=1)
    # abc operations
    matrices = [np.matrix(m) for m in preset.get("abc_matrices", {}).values()]
    a, b, c, e = _fully_symmetrize(matrices, a, b, c, e)
    # xyz operations
    x, y, z = abc_to_xyz(np.column_stack((a, b, c)), b_lattice).T
    matrices = [np.matrix(m) for m in preset.get("xyz_matrices", {}).values()]
    x, y, z, e = _fully_symmetrize(matrices, x, y, z, e)

    # ===== Plot ===== #
    # Process _strbool Arguements / 处理 _strbool 型参数
    plot_axis = _strbool(plot_axis)
    plot_arrow = _strbool(plot_arrow)
    plot_boundary = _strbool(plot_boundary)
    plot_path = _strbool(plot_path)
    plot_cbar = _strbool(plot_cbar)
    plot_legend = _strbool(plot_legend)

    # Figure Init / 绘图初始化
    figure = Figure(height=0.75, dpi=900)
    fig = figure.fig
    ax = figure.ax
    ax.axis("equal")

    # Plotter Init / 绘图器初始化
    plotter = _BandContourPlotter(x, y, e, cmap=colormap)
    bz_pltr = BrillouinZone2DPlotter.from_poscar(
        poscar,
        bravais_lattice_2d=bravais_lattice_2d,
    )
    bz_pltr.config["path_plot_kwargs"]["color"] = "black"
    if plot_config is not None:
        if not plot_config.exists():
            raise FileNotFoundError(f"No such file: {plot_config}")
        with open(plot_config, "rb") as f:
            plotter_config = tomllib.load(f)
        bz_pltr_config = plotter_config.pop("BrillouinZone2DPlotter", {})
        plotter.update_config(plotter_config)
        bz_pltr.update_config(bz_pltr_config)

    plotter.set_axis(ax, show=plot_axis)

    # Plot Contour Lines / 绘制等高线
    cline_lw = 0.3 if map_engine != "off" else 0.5
    match plot_cline.lower():
        case "off":
            pass
        case "colorful":
            colors = [get_colormap(colormap)(x) for x in np.linspace(0.03, 0.97, 7)]
            plotter.plot_tricontour(
                ax,
                linewidths=cline_lw,
                colors=colors,
            )
            plotter.config["colorbar_settings"]["axhline_kwargs"]["lw"] = cline_lw * 2
            plotter.config["colorbar_settings"]["axhline_kwargs"]["linestyle"] = "solid"
            plotter.config["colorbar_settings"]["axhline_kwargs"]["colors"] = colors
        case _:
            plotter.plot_tricontour(
                ax,
                linewidths=cline_lw,
                colors=plot_cline  # fmt: skip
            )
            plotter.config["colorbar_settings"]["axhline_kwargs"]["color"] = plot_cline

    # Process Map Engine
    map_engine = map_engine.lower()
    match map_engine:
        case "off":
            plotter.plot_tricontourf(ax, cmap=get_colormap("transparent"))
        case "tricontourf":
            plotter.plot_tricontourf(ax)
        case "tripcolor":
            plotter.plot_tripcolor(ax)
        case _:
            raise InvalidArgumentError(f"Invalid map_engine: {map_engine}")

    # Plot Colorbar / 绘制颜色条
    if plot_cbar:
        plotter.plot_colorbar(figure)
    # Plot Brillouin Zone / 绘制布里渊区
    bz_pltr.plot_boundary_step = plot_boundary
    bz_pltr.plot_path_step = plot_path
    bz_pltr.plot_point_step = plot_path
    bz_pltr.plot_point_text_step = plot_path
    bz_pltr.plot_base_vectors_step = plot_arrow
    bz_pltr.base_vectors_length = 0.8

    if plot_boundary:
        bz_pltr.plot_boundary(ax)
    if plot_path:
        try:
            bz_pltr.plot_path(ax)
        except HighSymmetryPoints2D.GammaAngleException as error:
            logger.warning(error)
            logger.warning(
                "`--plot-path` is set to False, try to specify the suitable `--preset` to avoid. "
            )
        else:
            bz_pltr.plot_point(ax)
            try:
                bz_pltr.plot_point_text(ax)
            except HighSymmetryPoints2D.LatticeGammaException:
                logger.debug(
                    "Meet LatticeGammaException, text change to Tepkit2024_tex style."
                )
                bz_pltr.hsps.text_style = "Tepkit2024_tex"
                bz_pltr.plot_point_text(ax)
    if plot_arrow:
        bz_pltr.plot_base_vectors(ax)

    # Plot Data Points / 绘制数据点
    if plot_point == "input":
        plotter.plot_input_data_points(ax, df)
    elif plot_point == "all":
        plotter.plot_all_data_points(ax, x, y)

    # Plot VBM/CBM Point / 绘制 VBM/CBM 点
    if index in ["vbe", "cbe"] and plot_bms != "off":
        np_points = np.array((x, y, z, e))
        if index == "vbe":
            m_label = "VBM"
            m_energy = df["energy"].max()
            m_energy_np = np.max(np_points[3])
            m_point = df.loc[df["energy"].idxmax()]
        elif index == "cbe":
            m_label = "CBM"
            m_energy = df["energy"].min()
            m_energy_np = np.min(np_points[3])
            m_point = df.loc[df["energy"].idxmin()]
        else:
            raise InvalidArgumentError(f"Invalid index: {index}")
        match plot_bms:
            case "all":
                # 标注对称化后所有数据的最值
                m_points = np_points[:, np_points[3] == m_energy_np]
            case "input":
                # 只标注输入数据的最值
                m_points = (m_point.k_x, m_point.k_y)
            case _:
                raise InvalidArgumentError(f"Invalid plot_bms: {plot_bms}")
        ax.plot(
            m_points[0],
            m_points[1],
            "o",
            label=m_label,
            color="black",
            markerfacecolor="white",
            markersize=3,
            markeredgewidth=0.5,
        )
        if plot_legend:
            plotter.plot_legend(figure)

    # Adjust Box / 调整显示范围
    scale = 2.0 if plot_arrow else 1.5
    ax.set_xlim(
        np.min((x, y)) * scale,
        np.max((x, y)) * scale,
    )
    ax.set_ylim(
        np.min((x, y)) * scale,
        np.max((x, y)) * scale,
    )

    # Save Figures / 保存图片
    save_name = f"{save_prefix}-{index}"
    save_dir = Path(save_dir)
    if spin in ["up", "down"]:
        save_name += f"-{spin}"
    if not save_dir.exists():
        save_dir.mkdir(parents=True)
    save_path = save_dir / f"{save_name}.png"
    plt.savefig(
        save_path,
        transparent=bool(colormap == "depth"),
    )
    logger.done(f"The picture was saved to {save_path}.")


if __name__ == "__main__":
    pass
