# 离散颜色
import matplotlib.pyplot as plt

tepkit_discrete_colormaps = {
    "tepkit_safe": {
        "red": "#FF6666",  # oklch(0.7044 0.1872 23.19)
        "blue": "#6699CC",  # oklch(0.6676 0.0939 249.39)
        "green": "#66CC00",  # oklch(0.7532 0.223 135.76)
        "yellow": "#FFCC00",  # oklch(0.8652 0.1768 90.38)
        "purple": "#9966CC",
        "orange": "#FF9933",
        "pink": "#FF99CC",
        "brown": "#CC9966",
        "cyan": "#66CCCC",
        "gray": "#999999",
    },
    "tepkit_smart": {
        "red": "#EE6666",  # oklch(0.6794 0.1687 22.65)
        "blue": "#7788CC",  # oklch(0.6414 0.1041 272.47)
        "green": "#44AA88",  # oklch(0.6688 0.1081 167.95)
        "yellow": "#FFBB00",  # oklch(0.8328 0.171572 82.0575)
        "purple": "#BB88EE",
        "orange": "#FF8833",
        "pink": "#EE99BB",
        "brown": "#DD9966",
        "cyan": "#55CCCC",
        "gray": "#999999",
    },
    "oklch_070_011": {
        "pink": "#d6809c",  # Hue 0
        "red": "#da8282",  # Hue 20
        "orange": "#d88669",  # Hue 40
        "brown": "#d08d54",  # Hue 60
        "yellow": "#b99b46",  # Hue 90
        "green": "#79af6d",  # Hue 140
        "cyan": "#2bb3b9",  # Hue 200
        "blue": "#769fe3",  # Hue 260
        "purple": "#ba8ac5",  # Hue 320
        "gray": "#9e9e9e",
    },
    "oklch_075_012": {
        "pink": "#ec8dab",  # Hue 0
        "red": "#f08e8e",  # Hue 20  +20
        "orange": "#eb9666",  # Hue 50  +30
        "brown": "#e39f50",  # Hue 80  +30
        "yellow": "#cbaa4b",  # Hue 90  +10
        "green": "#7bc27e",  # Hue 145  +55
        "cyan": "#2ac4cc",  # Hue 200  +55
        "blue": "#81aefa",  # Hue 260  +60
        "purple": "#ba9cef",  # Hue 300  +40
        "gray": "#aeaeae",
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
