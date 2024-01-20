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
from .line import Line


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
        input_file (str): input file path.
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

    @property
    def input_file(self) -> str | None:
        """Get input file path.

        Returns:
            str | None: input file path or None if not specified.
        """
        return self._input_file

    @input_file.setter
    def input_file(self, input_file: str | None) -> None:
        """Set input file path.

        Args:
            input_file (str | None): input file path.
        """
        if input_file is not None and not isinstance(input_file, str):
            raise TypeError("Input file path must be a string or None")

        self._input_file = input_file


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
        output_file: str,
        input_file: str | None = None
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
        self.input_file = input_file

        self._current_index: int
        self._input_data: dict[str, dict[str, list[int | float]]]

        self._saved = False  # Flag to check if data has been saved.
        self._setup()
        self._read_input_file()

    def _read_input_file(self) -> None:
        """Read input file."""
        if self._input_file is None:
            self._input_data = {}
            return

        with open(self._input_file, mode="r", encoding="utf-8") as fp:
            data = json.load(fp)

        for index in range(self._line_count):
            content = data.get(f"line_{index + 1}", {"x": [], "y": []})
            line_builder = self._lines[index].line_builder
            line_builder.x, line_builder.y = content.values()
            line_builder._plot_spline(*content.values())

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

        # Line storage setup:
        _colors = cycle(Line.COLORS)
        self._lines = [
            Line(
                self._ax,
                self._width,
                self._height,
                [],
                [],
                next(_colors)
            )
            for _ in range(self._line_count)
        ]

    def _select_line(self, event: Any) -> None:
        """Select a line to draw on.

        Args:
            event (Any): matplotlib event object.
        """
        if event.key.isnumeric() and 1 <= int(event.key) <= self.line_count:
            line_index = int(event.key) - 1

            # Disconnect current line and connect the selected one:
            self._lines[self._current_index].line_builder.disconnect()
            self._lines[line_index].line_builder.connect()
            self._current_index = line_index

            # Update plot title:
            self._fig.suptitle(
                "Click to add points for line number"
                + f" {self._current_index + 1}...",
                fontsize="large", fontweight="bold"
            )

    def _save(self) -> None:
        """Save data to JSON file."""
        data: dict[str, dict[str, list[int | float]]] = {
            f"line_{index + 1}": {
                "x": self._lines[index].line_builder.x,
                "y": self._lines[index].line_builder.y
            } for index in range(self._line_count)
        }

        try:
            with open(self._output_file, mode="w", encoding="utf-8") as fp:
                json.dump(data, fp, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            print(
                Fore.YELLOW + Style.BRIGHT
                + f"[Warning] Failed to save data in \"{self._output_file}\"."
                + f" Saving to \"{cfg.CLI.OUTPUT}\" instead..."
                + Style.RESET_ALL
            )

            with open(cfg.CLI.OUTPUT, mode="w", encoding="utf-8") as fp:
                json.dump(data, fp, ensure_ascii=False, indent=4)

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
        # Initial line selection:
        self._current_index = 0
        self._lines[self._current_index].line_builder.connect()

        # Initial plot titles:
        self._fig.suptitle(
            "Click to add points for line number"
            + f" {self._current_index + 1}...",
            fontsize="large",
            fontweight="bold"
        )
        self._ax.set_title(
            f"Press keys 1 to {self._line_count} to switch lines"
            + "\nClose the window, press ESC or Q to save and exit",
            fontsize="medium",
            fontstyle="italic"
        )

        # Full screen display:
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()  # type: ignore
        plt.grid(True)
        plt.show()
