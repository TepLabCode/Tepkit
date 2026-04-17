from pathlib import Path

import numpy as np
from matplotlib.patches import Polygon

from crysym2d.example_lattices import example_lattices_2d
from tepkit.utils.mpl_tools import Figure
from tepkit.utils.mpl_tools.plotters import Plotter


class Lattice2DPlotter(Plotter):
    def __init__(self, va, vb):
        super().__init__()
        self.va = va
        self.vb = vb
        self.config = {
            "point_color": "#17B",
        }

    def plot(self, ax):
        self.plot_lattice_points(ax)
        self.plot_base_vectors(ax)

    def plot_lattice_point(self, ax, a_i, b_i):
        x = a_i * self.va[0] + b_i * self.vb[0]
        y = a_i * self.va[1] + b_i * self.vb[1]
        ax.scatter(x, y, c=self.config["point_color"])

    def plot_lattice_points(self, ax, *, a_lim=(-1, 1), b_lim=(-1, 1), points=None):
        xs = []
        ys = []
        if points:
            for point in points:
                x = point[0] * self.va[0] + point[1] * self.vb[0]
                y = point[0] * self.va[1] + point[1] * self.vb[1]
                xs.append(x)
                ys.append(y)
        else:
            for a_i in range(a_lim[0], a_lim[1] + 1):
                for b_i in range(b_lim[0], b_lim[1] + 1):
                    x = a_i * self.va[0] + b_i * self.vb[0]
                    y = a_i * self.va[1] + b_i * self.vb[1]
                    xs.append(x)
                    ys.append(y)
        ax.scatter(xs, ys, c=self.config["point_color"])

    def plot_base_vectors(self, ax, length=None):
        """
        Plot the base vectors of the reciprocal lattice as arrows with dashed lines and green color.
        """
        length = length or 0.85
        b1 = np.array(self.va[:2]) * length
        b2 = np.array(self.vb[:2]) * length
        arrow_params = {
            "head_width": 0.2 * np.linalg.norm(b1),
            "head_length": 0.2 * np.linalg.norm(b1),
            "fc": "black",
            "ec": "black",
            "linewidth": 0.5,
        }
        text_params = {
            "textcoords": "offset points",
            "ha": "center",
            "va": "center",
        }
        ax.arrow(0, 0, b1[0], b1[1], **arrow_params)
        ax.arrow(0, 0, b2[0], b2[1], **arrow_params)
        ax.annotate(text=R"$\vec{a}$", xy=b1 * 0.95, xytext=(5, -12), **text_params)
        ax.annotate(text=R"$\vec{b}$", xy=b2 * 0.95, xytext=(-8, 15), **text_params)

    def plot_cell(self, ax, points=None, facecolor="#DDEEEEAA", edgecolor="#222"):
        """
        Plot a Polygon as cell.
        """
        points = points or [(0, 0), (1, 0), (1, 1), (0, 1)]
        xy_points = []
        for a_i, b_i in points:
            x = a_i * self.va[0] + b_i * self.vb[0]
            y = a_i * self.va[1] + b_i * self.vb[1]
            xy_points.append((x, y))
        polygon = Polygon(
            xy_points,
            facecolor=facecolor,
            edgecolor=edgecolor,
        )
        ax.add_patch(polygon)
        return polygon


if __name__ == "__main__":
    for lattice_name, lattice in example_lattices_2d.items():
        figure = Figure()
        ax = figure.ax
        pltr = Lattice2DPlotter(lattice[0], lattice[1])
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        a_lim = (-4, 4)
        b_lim = (-4, 4)
        match lattice_name:
            case "oc-eq-ac" | "oc-eq-ob":
                pltr.plot_cell(ax, [(0, 0), (1, 1), (0, 2), (-1, 1)], "#EEDDDDAA")
                # ax.set_xlim(-1.5, 2.5)
            case "oc-ne-ac":
                pltr.plot_cell(ax, [(0, 0), (1, 0), (0, 2), (-1, 2)], "#EEDDDDAA")
                ax.set_xlim(-1.5, 2.5)
                ax.set_ylim(-1, 3)
            case "oc-ne-ob":
                pltr.plot_cell(ax, [(0, 0), (1, 0), (2, 2), (1, 2)], "#EEDDDDAA")
                ax.set_xlim(-1.5, 2.5)
                ax.set_ylim(-1, 3)
            case "hp-ac":
                pltr.plot_cell(
                    ax,
                    [(0, 0), (1, 0), (1, 1), (0, 2), (-1, 2), (-1, 1)],
                    "#EEDDDDAA",
                )
                ax.set_xlim(-1.5, 2.5)
                ax.set_ylim(-1, 3)
            case "hp-ob":
                pltr.plot_cell(
                    ax,
                    [(0, 0), (1, 0), (2, 1), (2, 2), (1, 2), (0, 1)],
                    "#EEDDDDAA",
                )
                ax.set_xlim(-1.5, 2.5)
                ax.set_ylim(-1, 3)

        pltr.plot_cell(ax)
        pltr.plot_base_vectors(ax)
        pltr.plot_lattice_points(ax, a_lim=a_lim, b_lim=b_lim)

        ax.set_title(lattice_name)
        # pltr.save()
        pltr.close()
