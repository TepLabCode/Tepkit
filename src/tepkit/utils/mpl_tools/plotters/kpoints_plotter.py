from tepkit.io.vasp import ExplicitKpoints


class ExplicitKpoints2DPlotter:
    def __init__(self, kpoints: ExplicitKpoints):
        self.kpoints = kpoints
        self.color1 = "orange"
        self.color0 = "white"
        self.edge_color1 = "#444444"
        self.edge_color0 = "black"
        self.size1 = 2.5
        self.size0 = 1.8

    def plot(self, ax):
        df = self.kpoints.df
        points_weighted = df[df.k_weight != 0]
        points_zero_weighted = df[df.k_weight == 0]
        # 有权重的 SCF 点
        ax.plot(
            points_weighted.k_x,
            points_weighted.k_y,
            marker="o",
            markersize=self.size1,
            markerfacecolor=self.color1,
            linestyle="None",
            markeredgewidth=0.3,
            color=self.edge_color1,
        )
        # 无权重的能带点
        ax.plot(
            points_zero_weighted.k_x,
            points_zero_weighted.k_y,
            marker="o",
            markersize=self.size0,
            markerfacecolor=self.color0,
            linestyle="None",
            markeredgewidth=0.2,
            color=self.edge_color0,
        )
        return ax
