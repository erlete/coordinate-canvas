"""Canvas module.

Author:
    Paulo Sanchez (@erlete)
"""


import json
import os
from itertools import cycle
from typing import Any

import matplotlib.pyplot as plt
from colorama import Fore, Style

from .. import config as cfg
from .line_builder import _LineBuilder


class _CanvasProperties:
    """Canvas properties class.

    This class is only used to contain getters and setters for the canvas
    properties. Setters contain data type validation, but not value
    validation, as this functionality is meant to be used along with the CLI
    interface, which already validates the input data.

    Attributes:
        width (int | float): canvas width.
        height (int | float): canvas height.
        line_count (int): number of lines to draw on the canvas.
        output_file (str): output file path.
    """

    @property
    def width(self) -> int | float:
        """Get canvas width.

        Returns:
            int | float: canvas width.
        """
        return self._width

    @width.setter
    def width(self, width: int | float) -> None:
        """Set canvas width.

        Args:
            width (int | float): canvas width.
        """
        if not isinstance(width, (int, float)):
            raise TypeError("Canvas width must be an integer or a float")

        self._width = width

    @property
    def height(self) -> int | float:
        """Get canvas height.

        Returns:
            int | float: canvas height.
        """
        return self._height

    @height.setter
    def height(self, height: int | float) -> None:
        """Set canvas height.

        Args:
            height (int | float): canvas height.
        """
        if not isinstance(height, (int, float)):
            raise TypeError("Canvas height must be an integer or a float")

        self._height = height

    @property
    def line_count(self) -> int:
        """Get number of lines to draw on the canvas.

        Returns:
            int: number of lines to draw on the canvas.
        """
        return self._line_count

    @line_count.setter
    def line_count(self, line_count: int) -> None:
        """Set number of lines to draw on the canvas.

        Args:
            line_count (int): number of lines to draw on the canvas.
        """
        if not isinstance(line_count, int):
            raise TypeError("Number of lines must be an integer")

        self._line_count = line_count

    @property
    def output_file(self) -> str:
        """Get output file path.

        Returns:
            str: output file path.
        """
        return self._output_file

    @output_file.setter
    def output_file(self, output_file: str) -> None:
        """Set output file path.

        Args:
            output_file (str): output file path.
        """
        if not isinstance(output_file, str):
            raise TypeError("Output file path must be a string")

        self._output_file = output_file


class Canvas(_CanvasProperties):
    """Canvas class.

    This class is used to create a canvas where the user can draw lines by
    clicking on it. It uses matplotlib to draw the canvas and handle the
    events.

    Attributes:
        width (int | float): canvas width.
        height (int | float): canvas height.
        line_count (int): number of lines to draw on the canvas.
        output_file (str): output file path.
    """

    def __init__(
        self,
        width: int | float,
        height: int | float,
        line_count: int,
        output_file: str
    ) -> None:
        """Initialize a Canvas instance.

        Args:
            width (int | float): canvas width.
            height (int | float): canvas height.
            line_count (int): number of lines to draw on the canvas.
            output_file (str): output file path.
        """
        self.width = width
        self.height = height
        self.line_count = line_count
        self.output_file = output_file

        self._saved = False  # Flag to check if data has been saved.
        self._setup()

    def _setup(self) -> None:
        """Set up canvas configuration."""
        # Axis setup:
        self._ax = plt.gca()
        self._ax.set_xlim(0, self.width)
        self._ax.set_ylim(0, self.height)

        # Figure setup:
        self._fig = plt.gcf()
        self._fig.canvas.mpl_connect("key_press_event", self._select_line)
        self._fig.canvas.mpl_connect("key_release_event", self._exit)
        self._fig.canvas.mpl_connect("close_event", self._exit)

        plt.grid(True)

        # Data storage setup:
        self._data: dict[str, dict[str, list[int | float]]] = {
            f"line_{index}": {
                "x": [],
                "y": []
            } for index in range(1, self._line_count + 1)
        }

        _colors = cycle(cfg.COLORS)  # Temporary variable for colors.
        self._lines: list[dict[str, Any]] = [
            {
                "color": (color := next(_colors)),
                "line": (line := self._ax.plot(
                    [], [],
                    cfg.Link.SHAPE,
                    lw=cfg.Link.SIZE,
                    alpha=cfg.Link.ALPHA,
                    color=color
                )[0]),
                "line_builder": _LineBuilder(
                    line,
                    self._ax,
                    self._width,
                    self._height,
                    color
                )
            }
            for _ in range(self._line_count)
        ]

        self._current_data: list[Any] = [self._lines[0]["line"], 0]

    def _select_line(self, event: Any) -> None:
        """Select a line to draw on.

        Args:
            event (Any): matplotlib event object.
        """
        if event.key.isnumeric() and 1 <= int(event.key) <= self.line_count:
            self._lines[self._current_data[1]]["line_builder"].disconnect()
            self._lines[int(event.key) - 1]["line_builder"].connect()

            self._current_data[0] = self._lines[int(event.key) - 1].get("line")
            self._current_data[1] = int(event.key) - 1

            self._fig.suptitle(
                "Click to add points for line number"
                + f" {self._current_data[1] + 1}...",
                fontsize="large", fontweight="bold"
            )

    def _save(self) -> None:
        """Save data to JSON file."""
        for index in range(self._line_count):
            self._data[f"line_{index + 1}"]["x"].extend(
                self._lines[index]["line_builder"].x
            )
            self._data[f"line_{index + 1}"]["y"].extend(
                self._lines[index]["line_builder"].y
            )

        try:
            with open(self._output_file, mode="w", encoding="utf-8") as fp:
                json.dump(self._data, fp, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            print(
                Fore.YELLOW + Style.BRIGHT
                + f"[Warning] Failed to save data in \"{self._output_file}\"."
                + f" Saving to \"{cfg.CLI.OUTPUT}\" instead..."
                + Style.RESET_ALL
            )

    def _exit(self, event: Any) -> None:
        """Handle canvas exit events.

        This method handles the exit event of the canvas. It is called when the
        user presses the escape key, the q key or closes the canvas window. It
        saves the data to a JSON file and exits the program.

        Args:
            event (Any): matplotlib event object.
        """
        # If the event is a key press event, but not escape, ignore it:
        if hasattr(event, "key") and event.key != "escape":
            return

        if not self._saved:
            self._save()
            self._saved = True

        plt.close()

    def run(self) -> None:
        """Execute canvas functionality."""
        self._lines[0]["line_builder"].connect()

        self._fig.suptitle(
            "Click to add coordinates for the current line",
            fontsize="large",
            fontweight="bold"
        )
        self._ax.set_title(
            (
                f"Press keys 1 to {self._line_count} to switch lines"
                + "\nClose the window, press ESC or Q to save and exit"
            ),
            fontsize="medium",
            fontstyle="italic"
        )

        plt.show()
