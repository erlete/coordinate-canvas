"""Line builder module.

Author:
    Paulo Sanchez (@erlete)
"""


from typing import Any, Sequence

import matplotlib
from bidimensional import Coordinate
from bidimensional.functions import Spline
from colorama import Fore, Style

from .. import config as cfg


class _LineBuilder:
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

    def _plot_spline(self, x: Sequence[int | float], y: Sequence[int | float]) -> None:
        if len(x) > 1:
            sp = Spline([
                Coordinate(x_, y_)
                for x_, y_ in zip(x, y)
            ], gen_step=min(self.dimensions) / 100)

            x, y = zip(*sp.positions)

            sp.plot_input(
                cfg.Point.SHAPE,
                ms=cfg.Point.SIZE,
                alpha=cfg.Point.ALPHA,
                color=f"dark{self.color}",
            )

        elif len(x) == 1:
            self.ax.plot(
                x,
                y,
                cfg.Point.SHAPE,
                lw=cfg.Point.SIZE,
                alpha=cfg.Point.ALPHA,
                color=f"dark{self.color}"
            )

        self.line.set_data(x, y)
        self.line.figure.canvas.draw()

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

        # Duplicate coordinate prevention:
        if (
            len(self.x) > 0
            and (event.xdata, event.ydata) == (self.x[-1], self.y[-1])
        ):
            print(
                Fore.YELLOW + Style.BRIGHT
                + "[Warning] Skipping repetated coordinate "
                + f"({event.xdata}, {event.ydata})"
                + Style.RESET_ALL
            )
            return

        self.x.append(event.xdata)
        self.y.append(event.ydata)

        self._plot_spline(self.x, self.y)


class Line:

    COLORS = [
        "red",
        "green",
        "salmon",
        "blue",
        "orange",
        "violet",
        "goldenrod",
        "gray",
        "cyan"
    ]

    def __init__(
        self,
        ax: matplotlib.axes.Axes,
        width: float,
        height: float,
        x: list[int | float],
        y: list[int | float],
        color: str
    ) -> None:
        self._ax = ax
        self._width = width
        self._height = height
        self.color = color

        self._line = self._ax.plot(
            x,
            y,
            cfg.Link.SHAPE,
            lw=cfg.Link.SIZE,
            alpha=cfg.Link.ALPHA,
            color=color
        )[0]

        self._line_builder = _LineBuilder(
            self._line,
            self._ax,
            self._width,
            self._height,
            self._color
        )

    @property
    def color(self) -> str:
        """Get line color.

        Returns:
            color (str): line color.
        """
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        """Set line color.

        Args:
            value (str): line color.

        Raises:
            TypeError: if value is not a string.
            ValueError: if value is not a valid color.
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Invalid type '{type(value)}' for color. "
                + "Expected 'str'"
            )

        if not value in self.COLORS:
            raise ValueError(
                f"Invalid color '{value}'. "
                + f"Valid colors are: {', '.join(self.COLORS)}"
            )

        self._color = value

    @property
    def line(self) -> matplotlib.lines.Line2D:
        """Get line.

        Returns:
            line (matplotlib.lines.Line2D): line.
        """
        return self._line

    @property
    def line_builder(self) -> _LineBuilder:
        """Get line builder.

        Returns:
            line_builder (_LineBuilder): line builder.
        """
        return self._line_builder
