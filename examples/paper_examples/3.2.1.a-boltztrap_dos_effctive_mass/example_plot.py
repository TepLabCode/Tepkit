from pathlib import Path

from tepkit.io.boltztrap2 import Condtens
from tepkit.io.vasp import Poscar
from tepkit.utils.mpl_tools import Figure


class Plotter:
    def __init__(self, condtens):
        self.condtens = condtens
        self.xlim = {"h": (1e8, 1e15), "e": (1e8, 1e15)}

    def plot(self, carrier_type, direction, loc=None):
        figure = Figure(height=0.5)
        figure.adjust_margin(right=100, bottom=300)
        ax = figure.ax
        for t in [300, 500, 700]:
            self.condtens.plot(
                ax,
                "log-rho",
                "m_eff",
                t=t,
                y_direction=direction,
                carrier_type=carrier_type,
                label=f"{t} K",
            )
        ax.grid()
        ax.set_xlim(*self.xlim[carrier_type])
        ax.set_ylim(0, 2)
        figure.add_legend(fontsize=6, loc=loc)
        figure.set_locator("y", "gap", ax.get_ylim()[1] / 5)
        figure.set_locator("y", "gap", ax.get_ylim()[1] / 10, minor=True)
        figure.save(f"EffMass-{carrier_type}-{direction}.png")
        return figure


def main(path, xlim):
    path = Path(path)
    condtens = Condtens.from_dir(path)
    poscar = Poscar.from_dir(path)
    lattice = poscar.get_lattice()
    condtens.calculate_average_effective_mass(
        "m_e", volume=poscar.get_volume(unit="m^3")
    )
    condtens.calculate_carrier_density(
        lattice=poscar.lattice,
        dimension=2,
        abs_density=True,
    )
    plotter = Plotter(condtens=condtens)
    plotter.xlim = xlim
    plotter.plot("h", "x")
    plotter.plot("e", "x")
    # plotter.plot("h", "y")
    # plotter.plot("e", "y")


if __name__ == "__main__":
    main(
        path=R"input-boltztrap2",
        xlim={"h": (5e11, 1e15), "e": (5e10, 1e14)},
    )
