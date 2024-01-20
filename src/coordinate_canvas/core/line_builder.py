"""Line builder module.

Author:
    Paulo Sanchez (@erlete)
"""


from typing import Any

import matplotlib
from bidimensional import Coordinate
from bidimensional.functions import Spline
from colorama import Fore, Style

from .. import config as cfg


class LineBuilder:
    """Line builder on click events.

    This class is used to build a line based on click events. line is
    built by clicking on the matplotlib plot. coordinates are stored
    in a list of tuples.
    """

    def __init__(
        self,
        line: Any,
        ax: matplotlib.axes.Axes,
        width: float,
        height: float,
        color: str
    ) -> None:
        """Initialize a LineBuilder instance.

        Args:
            line (Any): line to be built.
            ax (matplotlib.axes.Axes): axes where the line is drawn.
            width (float): width of the plot.
            height (float): height of the plot.
            color (str): color of the line.
        """
        self.line = line
        self.ax = ax
        self.dimensions = (width, height)
        self.color = color

        self.x, self.y = list(line.get_xdata()), list(line.get_ydata())
        self.cid = None
        self.line.figure.canvas.draw()

    def is_connected(self) -> bool:
        """Check if the line builder is connected.

        Returns:
            cid (bool): whether the line builder is connected or not.
        """
        return self.cid is not None

    def connect(self) -> None:
        """Connect line builder to matplotlib plot."""
        self.cid = self.line.figure.canvas.mpl_connect(
            "button_press_event",
            self
        )

    def disconnect(self) -> None:
        """Disconnect line builder from matplotlib plot."""
        self.line.figure.canvas.mpl_disconnect(self.cid)

    def __call__(self, event: matplotlib.backend_bases.MouseEvent) -> None:
        """Click event handler.

        This method is called on every click event. It adds the coordinates to
        the list of coordinates and updates the line.

        Args:
            event (matplotlib.backend_bases.MouseEvent): click event.
        """
        # Axes validation:
        if event.inaxes != self.line.axes:
            return

        # Prevent single-coordinate spline error:
        if len(self.x) > 0:

            # Ignore repeated coordinates:
            if (
                event.xdata != self.x[-1]
                or event.ydata != self.y[-1]
            ):
                self.x.append(event.xdata)
                self.y.append(event.ydata)

                if len(self.x) > 1:
                    sp = Spline([
                        Coordinate(x_, y_)
                        for x_, y_ in zip(self.x, self.y)
                    ], gen_step=min(self.dimensions) / 100)

                    x = [x_ for x_, _ in sp.positions]
                    y = [y_ for _, y_ in sp.positions]

                    sp.plot_input(
                        cfg.Input.SHAPE,
                        ms=cfg.Input.SIZE,
                        alpha=cfg.Input.ALPHA,
                        color=f"dark{self.color}",
                    )

                    self.line.set_data(x, y)
                    self.line.figure.canvas.draw()

            else:
                print(
                    Fore.YELLOW + Style.BRIGHT
                    + "[Warning] Skipping repetated coordinate "
                    + f"({event.xdata}, {event.ydata})"
                    + Style.RESET_ALL
                )

        else:
            self.ax.plot(
                # Prevent None values with default empty list:
                event.xdata or [],
                event.ydata or [],
                cfg.Input.SHAPE,
                lw=cfg.Input.SIZE,
                alpha=cfg.Input.ALPHA,
                color=f"dark{self.color}"
            )

            self.x.append(event.xdata)
            self.y.append(event.ydata)

            self.line.set_data(self.x, self.y)
            self.line.figure.canvas.draw()
