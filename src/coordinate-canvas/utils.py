"""Simple manual coordinate generator.

Allows the user to generate coordinates by clicking on the matplotlib plot.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


from bidimensional import Coordinate
from bidimensional.functions import Spline
from matplotlib import pyplot as plt
import matplotlib

from .config import CONFIG


class LineBuilder:
    """Builds a line based on click event handlers.

    This class is used to build a line based on click events. The line is
    built by clicking on the matplotlib plot. The coordinates are stored
    in a list of tuples.
    """

    CONFIG = CONFIG

    def __init__(self, line: matplotlib.lines.Line2D,
                 ax: matplotlib.axes.Axes,
                 width: float, height: float, color: str) -> None:

        self.line = line
        self.ax = ax
        self.width = width
        self.height = height
        self.color = color

        self.x, self.y = list(line.get_xdata()), list(line.get_ydata())

        self.cid = line.figure.canvas.mpl_connect("button_press_event", self)
        self.line.figure.canvas.draw()

    def __call__(self, event) -> None:
        if event.inaxes != self.line.axes:
            return

        self.x.append(event.xdata)
        self.y.append(event.ydata)

        if len(self.x) > 1:
            sp = Spline([
                Coordinate(x_, y_)
                for x_, y_ in zip(self.x, self.y)
            ], gen_step=min(self.width, self.height) / 100)

            x = [x_ for x_, _ in sp.positions]
            y = [y_ for _, y_ in sp.positions]

            sp.plot_input(
                CONFIG.get("input").get("shape"),
                ms=CONFIG.get("input").get("size"),
                alpha=CONFIG.get("input").get("alpha"),
                color=f"dark{self.color}",
            )

        else:
            x, y = self.x, self.y
            self.ax.plot(
                x, y,
                CONFIG.get("input").get("shape"),
                lw=CONFIG.get("input").get("size"),
                alpha=CONFIG.get("input").get("alpha"),
                color=f"dark{self.color}"
            )

        self.line.set_data(x, y)
        self.line.figure.canvas.draw()
