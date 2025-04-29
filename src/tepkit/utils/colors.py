# 离散颜色
import matplotlib.pyplot as plt

tepkit_discrete_colormaps = {
    "tepkit_safe": {
        "red": "#FF6666",
        "blue": "#6699CC",
        "green": "#66CC00",
        "yellow": "#FFCC00",
        "purple": "#9966CC",
        "orange": "#FF9933",
        "pink": "#FF99CC",
        "brown": "#CC9966",
        "cyan": "#66CCCC",
        "gray": "#999999",
    },
    "tepkit_smart": {
        "red": "#EE6666",
        "blue": "#7788CC",
        "green": "#44AA88",
        "yellow": "#FFBB00",
        "purple": "#BB88EE",
        "orange": "#FF8833",
        "pink": "#EE99BB",
        "brown": "#DD9966",
        "cyan": "#55CCCC",
        "gray": "#999999",
    },
}

# 别名
tepkit_colors = tepkit_discrete_colormaps["tepkit_smart"]

# 平滑色谱
_tepkit_smooth_colormaps = {
    "transparent": [
        (0.0, "#00000000"),
        (1.0, "#00000000"),
    ],
    "excel_rdylgn": [
        (0.0, "#F8696B"),
        (0.5, "#FFEB84"),
        (1.0, "#63BE7B"),
    ],
    "depth": [
        (0.0, "#000000"),
        (1.0, "#EEEEEE"),
    ],
    "tepkit_rainbow": [
        (0 / 6, tepkit_colors["purple"]),  # #BB88EE
        (1 / 6, tepkit_colors["blue"]),  #   #7788CC
        (2 / 6, tepkit_colors["cyan"]),  #   #55CCCC
        (3 / 6, tepkit_colors["green"]),  #  #44AA88
        (4 / 6, tepkit_colors["yellow"]),  # #FFBB00
        (5 / 6, tepkit_colors["orange"]),  # #FF8833
        (6 / 6, tepkit_colors["red"]),  #    #EE6666
    ],
    "tepkit_rainbow_ex": [
        (0.00, "#9966CC"),
        (0.05, "#6688CC"),
        (0.20, "#00BBBB"),
        (0.40, "#66EE88"),
        (0.60, "#EEEE44"),
        (0.80, "#FF7744"),
        (0.95, "#EE5555"),
        (1.00, "#FF99DD"),
    ],
    "tepkit_heat": [
        (0.00, "#222222"),
        (0.05, "#333333"),
        (0.10, "#003366"),
        (0.15, "#004477"),
        (0.20, "#225588"),
        (0.30, "#00BBBB"),
        (0.45, "#66FF88"),
        (0.65, "#EEEE44"),
        (0.90, "#FF7744"),
        (1.00, "#FF5555"),
    ],
}

# 生成反转的 colormap
_tepkit_smooth_colormaps_r = {
    f"{name}_r": [(1 - color[0], color[1]) for color in reversed(colormap)]
    for name, colormap in _tepkit_smooth_colormaps.items()
}

# 合并 colormap
tepkit_smooth_colormaps: dict[str, list[tuple[float, str]]] = (
    _tepkit_smooth_colormaps | _tepkit_smooth_colormaps_r
)

if __name__ == "__main__":
    import numpy as np
    from tepkit.utils.mpl_tools import Figure
    from tepkit.utils.mpl_tools.color_tools import get_colormap

    figure = Figure()
    ax = figure.ax
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    for i, cmap_name in enumerate(["tepkit_rainbow_ex", "tepkit_rainbow", "rainbow"]):
        cmap = get_colormap(cmap_name)
        ax.imshow(
            gradient,
            aspect="auto",
            cmap=cmap,
            extent=(0, 1, i / 10, (i + 1) / 10),
        )

    plt.ylim(0, 1)
    figure.show()
