from tepkit.utils.colors import (
    tepkit_discrete_colormaps,
    tepkit_smooth_colormaps,
    tepkit_colors,
)
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

Colormap = ListedColormap | LinearSegmentedColormap | str


def get_colormap(style: str) -> Colormap:
    """
    根据名称返回 Colormap
    """
    if style in tepkit_discrete_colormaps.keys():
        return ListedColormap(tepkit_discrete_colormaps[style].values())
    elif style in tepkit_smooth_colormaps.keys():
        return LinearSegmentedColormap.from_list(style, tepkit_smooth_colormaps[style])
    else:
        return style


def get_colors(style: str = "tepkit_smart") -> list[str]:
    """
    根据风格名称返回颜色列表
    """
    return tepkit_discrete_colormaps[style].values()


def get_color(name: str, style: str = "tepkit_smart") -> str:
    """
    根据颜色名称返回颜色值
    """
    return tepkit_discrete_colormaps[style][name]


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    from tepkit import package_root

    plt.style.use(package_root / "utils/mpl_tools/styles" / "tepkit_basic.mplstyle")

    def test1():
        cmap = get_colormap("tepkit_safe")
        data = np.arange(100)[::-1].reshape(10, 10)
        plt.imshow(data, cmap=cmap, alpha=0.7)  # 绘制热图，使用 'viridis' 颜色映射
        plt.colorbar()  # 添加 colorbar
        plt.show()

    def test2():
        cmap = get_colormap("tepkit_rainbow")
        data = np.arange(21)[::-1].reshape(7, 3)
        plt.imshow(data, cmap=cmap)  # 绘制热图，使用 'viridis' 颜色映射
        plt.colorbar()  # 添加 colorbar
        plt.show()

    def test3():
        x = np.linspace(0, 1)
        y = np.sin(x * np.pi)

        for name, color in tepkit_colors["tepkit_smart"].items():
            plt.plot(x, y, c=color, label=name.capitalize(), lw=1.8, alpha=0.8)
            y = y * 0.9 - 0.1
        plt.legend(bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.xlim(0, 1)
        plt.ylim(-1, 1.2)
        plt.show()

    def test4():
        cmap = get_colormap("tepkit_smart")
        N = 100
        x = np.random.rand(N)
        y = np.random.rand(N)
        colors = np.random.rand(N)
        area = np.pi * (10 * np.random.rand(N)) ** 2  # 0 to 15 point radii

        plt.scatter(x, y, s=area, c=colors, cmap=cmap, alpha=0.7)
        plt.show()

    def test5():
        plt.bar(
            range(10),
            np.random.rand(10),
            color=get_colors("tepkit_smart"),
            alpha=0.8,
        )
        categories = [x.capitalize() for x in tepkit_colors["tepkit_smart"].keys()]
        plt.xticks(range(len(categories)), categories, rotation=60, ha="right")
        plt.show()

    test1()
    test2()
    test3()
    test4()
    test5()
