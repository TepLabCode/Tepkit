import numpy as np
from tepkit.core.high_symmetry_points import HighSymmetryPoints2D
from tepkit.core.symmetry import BravaisLattice2D
from tepkit.io.vasp import Poscar
from tepkit.utils.typing_tools import NumpyArray3x3
from tepkit.utils.mpl_tools.plotters.plotter import Plotter


class BrillouinZone2DPlotter(Plotter):
    """
    绘制二维布里渊区的类。
    可以绘制二维布里渊区的边界、高对称点、高对称路径、基矢量等。
    """

    def __init__(
        self,
        b_lattice: NumpyArray3x3,
        bravais_lattice_2d: BravaisLattice2D | None = None,
    ):
        super().__init__()
        # Read Input Data
        self.b_lattice: NumpyArray3x3 = np.array(b_lattice)
        self.bravais_lattice_2d: BravaisLattice2D | None = bravais_lattice_2d
        # Add Data
        hsps = HighSymmetryPoints2D(b_lattice=self.b_lattice)
        self.boundary_data = hsps.get_dict("token", "k_xyz", hsps.get_boundary_tokens())
        self.data = hsps.get_dict("token", "k_xyz")
        # self.points: NumpyArrayNx3 = np.array([np.array(i) for i in data])
        # The position offset of the text labels / 通用文字偏移量
        xytext_settings = {
            "G"  : (+5, -7),
            "A"  : (+8, -7),
            "AR" : (-8, +0),
            "B"  : (+8, +7),
            "BR" : (+5, -5),
            "C1" : (+7, +7),
            "C2" : (-7, +7),
            "C3" : (+5, -5),
            "C4" : (+5, -5),
            "C1A": (+8, -5),
            "C1B": (-5, +7),
            "C2A": (-8, -5),
            "C2B": (+5, +7),
            "C3A": (+5, -5),
            "C3B": (+5, -5),
            "C4A": (+5, -5),
            "C4B": (+5, -5),
            "D1" : (+7, +7),
            "D2" : (-7, +7),
            "D3" : (+5, -5),
            "D4" : (+5, -5),
        }  # fmt:skip
        # 不同格子类型的精调偏移量
        match self.bravais_lattice_2d:
            case BravaisLattice2D.hp:
                xytext_settings["A"] = (10, -3)
                xytext_settings["D1"] = (8, 4)
            case BravaisLattice2D.oc:
                xytext_settings["C1"] = (9, -3)
                xytext_settings["C1B"] = (10, 3)
                xytext_settings["C2"] = (0, 7)
                xytext_settings["C2B"] = (9, 5)
                xytext_settings["B"] = (9, -1)
                xytext_settings["G"] = (-7, -8)
                xytext_settings["D1"] = (7, -8)
        self.config: dict = {
            "xytext_settings": xytext_settings,
            "paths_tokens": None,
            "token_texts": None,
            "path_plot_kwargs": {
                "color": "orange",
                "lw": None,
                "linestyle": None,
                "alpha": None,
            },
            "boundary_plot_kwargs": {
                "color": "black",
                "lw": None,
                "linestyle": None,
                "alpha": None,
            },
            "point_text_fontsize": 8,
        }
        self.hsps = HighSymmetryPoints2D(
            b_lattice=self.b_lattice,
            bravais_lattice_2d=self.bravais_lattice_2d,
        )
        # Options
        self.plot_boundary_step = True
        self.plot_path_step = True
        self.plot_point_step = True
        self.plot_point_text_step = True
        self.plot_base_vectors_step = True
        self.base_vectors_length = 1.0

    @classmethod
    def from_poscar(
        cls,
        poscar: Poscar,
        with_2pi: bool = True,
        bravais_lattice_2d=None,
        sym_prec=1e-5,
    ):
        """
        Instantiation a Plotter by a Poscar.
        """
        if bravais_lattice_2d == "auto":
            bravais_lattice_2d = BravaisLattice2D.from_poscar(poscar, sym_prec=sym_prec)
        obj = cls(
            b_lattice=poscar.get_reciprocal_lattice(with_2pi=with_2pi),
            bravais_lattice_2d=bravais_lattice_2d,
        )
        return obj

    def plot(self, ax):
        if self.plot_boundary_step:
            self.plot_boundary(ax)
        if self.bravais_lattice_2d is not None:
            if self.plot_path_step:
                self.plot_path(ax)
            if self.plot_point_step:
                self.plot_point(ax)
            if self.plot_point_text_step:
                self.plot_point_text(ax)
        if self.plot_base_vectors_step:
            self.plot_base_vectors(ax)
        ax.axis("equal")

    def plot_boundary(self, ax):
        """
        Plot the boundary of the first Brillouin zone.
        """
        hsps = self.hsps
        tokens = hsps.get_boundary_tokens()
        kx = hsps.get_list("k_x", tokens)
        ky = hsps.get_list("k_y", tokens)
        ax.plot(kx, ky, **self.config["boundary_plot_kwargs"])

    def plot_path(self, ax):
        """
        Plot the high-symmetriy paths.
        """
        hsps = self.hsps
        paths_tokens = self.config["paths_tokens"] or hsps.get_paths_tokens()
        for path_tokens in paths_tokens:
            kx = hsps.get_list("k_x", path_tokens)
            ky = hsps.get_list("k_y", path_tokens)
            ax.plot(kx, ky, **self.config["path_plot_kwargs"])

    def plot_point(self, ax):
        """
        Plot the high-symmetriy points.
        """
        hsps = self.hsps
        paths_tokens = self.config["paths_tokens"] or hsps.get_paths_tokens()
        for path_tokens in paths_tokens:
            kx = hsps.get_list("k_x", path_tokens)
            ky = hsps.get_list("k_y", path_tokens)
            ax.plot(kx, ky, "o", color="black", markersize=2.3)

    def plot_point_text(self, ax):
        """
        Plot the name of the high-symmetriy points.
        """
        hsps = self.hsps
        paths_tokens = self.config["paths_tokens"] or hsps.get_paths_tokens()
        token_to_text = hsps.get_dict("token", "text")
        token_to_text.update(self.config["token_texts"] or {})
        token_to_xy = hsps.get_dict("token", "k_xy")
        token_to_xytext = self.config["xytext_settings"]
        for path_tokens in paths_tokens:
            for token in path_tokens:
                ax.annotate(
                    text=token_to_text[token],
                    xy=token_to_xy[token],
                    xytext=token_to_xytext[token],
                    textcoords="offset points",
                    ha="center",
                    va="center",
                    fontsize=self.config["point_text_fontsize"],
                )

    def plot_base_vectors(self, ax, length=None):
        """
        Plot the base vectors of the reciprocal lattice as arrows with dashed lines and green color.
        """
        length = length or self.base_vectors_length
        b1 = self.b_lattice[0][:2] * length
        b2 = self.b_lattice[1][:2] * length
        arrow_params = {
            "head_width": 0.05 * np.linalg.norm(b1),
            "head_length": 0.07 * np.linalg.norm(b1),
            "fc": "grey",
            "ec": "grey",
            "linewidth": 0.5,
        }
        text_params = {
            "textcoords": "offset points",
            "ha": "center",
            "va": "center",
        }
        ax.arrow(0, 0, b1[0], b1[1], **arrow_params)
        ax.arrow(0, 0, b2[0], b2[1], **arrow_params)
        ax.annotate(text=R"$\vec{b}_1$", xy=b1 * 0.95, xytext=(2, -8), **text_params)
        ax.annotate(text=R"$\vec{b}_2$", xy=b2 * 0.95, xytext=(8, 0), **text_params)

    def to_png(self):
        pass


if __name__ == "__main__":
    pass
