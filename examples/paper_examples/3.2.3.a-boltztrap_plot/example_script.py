from tepkit.io.boltztrap2 import Condtens
from tepkit.io.vasp import Poscar
from tepkit.utils.mpl_tools import Figure

# Read Files
condtens = Condtens.from_dir(R".\input-boltztrap2")
poscar = Poscar.from_dir(R".\input-boltztrap2")
# Effective Thickness Correction
proportion = poscar.thickness_info["effective_thickness_proportion"]
condtens.effective_thickness_correction(proportion=proportion)
# Relaxation Time
# Ref: https://pubs.acs.org/doi/10.1021/acsenergylett.6b00289
condtens.add_relaxation_time(21.3, 300, "x", "e", with_inverse_proportion=True)
condtens.add_relaxation_time(21.3, 300, "x", "h", with_inverse_proportion=True)
condtens.add_relaxation_time(21.3, 300, "y", "e", with_inverse_proportion=True)
condtens.add_relaxation_time(21.3, 300, "y", "h", with_inverse_proportion=True)
condtens.multiply_relaxation_time()
# Carrier Density
lattice = poscar.get_lattice()
condtens.calculate_carrier_density(
    lattice=poscar.lattice,
    dimension=2,
    abs_density=True,
)
# Unit Conversion
for d in ["xx", "yy"]:
    condtens.df[("S", "μV/K", d)] = condtens.df[("S", "V/K", d)] * 1e6
    condtens.df[("sigma", "$10^6$ S/m", d)] = condtens.df[("sigma", "S/m", d)] / 1e6
    condtens.df[("PF", "mW/(m*K^2)", d)] = condtens.df[("PF", "W/(m*K^2)", d)] * 1e3
y_units = {
    "S": "μV/K",
    "sigma": "$10^6$ S/m",
    "PF": "mW/(m*K^2)",
}
condtens.label_texts["W/(m*K)"] = R"W m$^{-1}$ K$^{-1}$"
condtens.label_texts["mW/(m*K^2)"] = R"mW m$^{-1}$ K$^{-2}$"


# Plot Figures
def plot_figure(ts, qualtity, direction, carrier, save_name, legend=False):
    figure = Figure(height=0.6)
    ax = figure.ax
    for t in ts:
        condtens.plot(
            figure.ax,
            x="log-rho",
            y=qualtity,
            t=t,
            y_direction=direction,
            y_unit=y_units.get(qualtity, None),
            carrier_type=carrier,
            label=f"T={t} K",
        )
    ax.grid()
    # x-axis range
    match carrier:
        case "h":
            ax.set_xlim(5e11, 2e14)
        case "e":
            ax.set_xlim(5e9, 2e12)
    # y-axis range
    match qualtity:
        case "S":
            match carrier:
                case "h":
                    ax.set_ylim(0, 800)
                case "e":
                    ax.set_ylim(-800, 0)
        case "sigma":
            ax.set_ylim(0, 4e6)
        case "log-sigma":
            ax.set_ylim(10, 1e7)
        case "kappae":
            ax.set_ylim(0, 20)
        case "log-kappae":
            ax.set_ylim(1e-4, 1e2)
        case "PF":
            ax.set_ylim(0, 10)
    figure.adjust_margin(bottom=300)
    if legend:
        figure.add_legend()
    figure.save(save_name)


qualtities = ["S", "log-sigma", "log-kappae", "PF"]
ts = [300, 500, 700]
for qualtity in qualtities:
    for carrier in ["h", "e"]:
        for direction in ["x"]:
            print(f"{qualtity}-{carrier}")
            plot_figure(
                ts=ts,
                qualtity=qualtity,
                direction=direction,
                carrier=carrier,
                save_name=f"{qualtity}-{carrier}",
                legend=True,
            )
