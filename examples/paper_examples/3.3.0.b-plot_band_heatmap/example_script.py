from tepkit.functions.vasp import band_contour
from tepkit.io.vasp import Eigenval

data_dir = R"input"

band_contour(
    data_dir=data_dir,
    save_prefix="HeatMap",
    index="VBE",
    preset="auto",
    ref="midgap",
    plot_path="on",
    plot_arrow="off",
)

band_contour(
    data_dir=data_dir,
    save_prefix="ContourMap",
    index="VBE",
    preset="auto",
    ref="midgap",
    plot_path="on",
    plot_arrow="off",
    map_engine="off",
    plot_cline="colorful",
)

band_contour(
    data_dir=data_dir,
    save_prefix="ColorTexture",
    index="VBE",
    preset="auto",
    ref="midgap",
    plot_path="off",
    plot_arrow="off",
    plot_cline="off",
    plot_bms="off",
    plot_cbar="off",
    plot_boundary="off",
)

band_contour(
    data_dir=data_dir,
    save_prefix="DepthMap",
    index="VBE",
    preset="auto",
    ref="midgap",
    plot_path="off",
    plot_arrow="off",
    plot_cline="off",
    plot_bms="off",
    colormap="depth",
    plot_cbar="off",
    plot_boundary="off",
)
