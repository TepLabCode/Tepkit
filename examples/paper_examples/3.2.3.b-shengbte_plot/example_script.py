from pathlib import Path

import matplotlib.pyplot as plt
from tepkit.io.shengbte import (
    CumulativeKappaTensor,
    CumulativeKappaVsOmegaTensor,
    Gruneisen,
    KappaTensorVsT,
    Omega,
    V,
    W,
)
from tepkit.io.vasp import Poscar
from tepkit.utils.colors import tepkit_colors
from tepkit.utils.mpl_tools import Figure

# Read Files
job_dir = Path(R"./input-shengbte")

# Effective Thickness Correction
poscar = Poscar.from_dir(job_dir)
proportion = poscar.thickness_info["effective_thickness_proportion"]

# KappaTensorVsT
kappal = KappaTensorVsT.from_dir(job_dir)
kappal.effective_thickness_correction(proportion=proportion)
figure = Figure(height=0.8)
plt.xlabel("$T$ (K)")
plt.ylabel(R"$κ_\mathrm{lat}$ (W m$^{-1}$ K$^{-1}$)")
plt.xlim(100, 1000)
plt.ylim(0, 8)
plt.grid(True)
kappal.plot(figure.ax, direction="xx", color="#78B")
figure.set_locator("x", "gap", 300)
figure.set_locator("x", "gap", 100, minor=True)
figure.set_locator("y", "gap", 2)
figure.set_locator("y", "gap", 1, minor=True)
figure.save("KappaTensorVsT.png")

# CumulativeKappaTensor
ckappal = CumulativeKappaTensor.from_dir(job_dir, t=300)
ckappal.effective_thickness_correction(proportion=proportion)
figure = Figure(height=0.8)
plt.xlabel("Mean Free Path (nm)")
plt.ylabel(R"$κ_\mathrm{lat}^\mathrm{cumulative}$ (W m$^{-1}$ K$^{-1}$)")
plt.xscale("log")
plt.xlim(1e-2, 1e6)
plt.ylim(-0.5, 3)
plt.grid(True)
ckappal.plot(figure.ax, direction="xx", fit=True, x0=True, color="#78B")
figure.set_locator("y", "gap", 1, minor=True)
figure.save("CumulativeKappaTensor-300K.png")

# CumulativeKappaVsOmegaTensor
ckappalo = CumulativeKappaVsOmegaTensor.from_dir(job_dir, t=300)
ckappalo.effective_thickness_correction(proportion=proportion)
figure = Figure(height=0.8)
plt.xlabel("Frequency (THz)")
plt.ylabel(R"$κ_\mathrm{lat}^\mathrm{cumulative}$ (W m$^{-1}$ K$^{-1}$)")
plt.xlim(0, 4.5)
plt.ylim(-0.5, 3)
plt.grid(True)
ckappalo.plot(figure.ax, direction="xx", y_unit="THz", color="#78B")
figure.set_locator("x", "gap", 1)
figure.set_locator("y", "gap", 1, minor=True)
figure.save("CumulativeKappaVsOmegaTensor-300K.png")

# Omega (Angular frequenc)
omega = Omega.from_dir(job_dir)
colors = list(tepkit_colors.values())
colors[3] = tepkit_colors["brown"]

# V (Group velocity)
v = V.from_dir(job_dir)
v.omega = omega
figure = Figure(height=0.8)
plt.xlabel("Frequency (THz)")
plt.ylabel(R"Group Velocity (km/s)")
plt.xlim(0, 4.5)
plt.ylim(0.5, 3)
plt.grid(True)
v.plot(figure.ax, direction="speed", x_unit="THz", colors=colors, group="ztlo")
figure.add_legend(font_size=6)
figure.save("Frequency-GroupVelocity.png")

# Gruneisen (Grüneisen parameter)
gruneisen = Gruneisen.from_dir(job_dir)
gruneisen.omega = omega
figure = Figure(height=0.8)
plt.xlabel("Frequency (THz)")
plt.ylabel(R"Grüneisen Parameter")
plt.xlim(0, 4.5)
plt.ylim(-1, 7)
plt.grid(True)
gruneisen.plot(figure.ax, x_unit="THz", colors=colors, group="ztlo")
figure.set_locator("y", "gap", 1, minor=True)
figure.add_legend(font_size=6)
figure.save("Frequency-GruneisenParameter.png")

# W (Scattering rate)
w = W.from_dir(job_dir, t=300)
w.omega = omega
figure = Figure(height=0.8)
plt.xlabel("Frequency (THz)")
plt.ylabel(R"Scattering Rate (1/ps)")
plt.yscale("log")
plt.xlim(0, 4.5)
plt.ylim(1e-4, 1e3)
plt.grid(True)
w.plot(figure.ax, direction="speed", x_unit="THz", colors=colors, group="ztlo")
figure.set_locator("y", "half-log", minor=True)
figure.add_legend(font_size=6)
figure.save("Frequency-ScatteringRate-300K.png")
