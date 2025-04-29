# Plotting Figures

## Style

To make it easier to plot beautiful figures, Tepkit include a matplotlib style sheets file.

It can be used as follows:

```python
import matplotlib.pyplot as plt
from tepkit import package_root
plt.style.use(package_root / "utils/mpl_tools/styles/tepkit_basic.mplstyle")
```
For more information, please check:

- [Customizing Matplotlib with style sheets and rcParams | Matplotlib documentation](https://matplotlib.org/stable/users/explain/customizing.html#defining-your-own-style)

## Figure

Tepkit provides a `Figure` class that makes matplotlib easier to use.

The simplest usage of it is as follows:

```python
from tepkit.utils.mpl_tools import Figure
figure = Figure()
fig = figure.fig # matplotlib.figure.Figure
ax = figure.ax # matplotlib.axes.Axes
```

For more detail, please check: [tepkit.utils.mpl_tools.Figure](/autoapi/tepkit/utils/mpl_tools/Figure)

## Plotter

TODO
