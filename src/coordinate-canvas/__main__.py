"""Main executable script for the coordinate-canvas module.

This script is the main executable script for the coordinate-canvas module. It
is used to draw lines on a matplotlib plot and save the coordinates of the
points that compose the lines.

Notes:
    This script saves an output file named "coordinates.json" in the current
    working directory. Said directory is the same over which the module is
    executed via the command line.

Author:
    Paulo Sanchez (@erlete)
"""


import json
import sys
from itertools import cycle

import matplotlib.pyplot as plt
from bidimensional import Coordinate
from bidimensional.functions import Spline

from .core.config import COLORS, INPUT, POSITIONS
from .core import input_handler as ih
from .core.line_builder import LineBuilder


# Constants' definition:

COLORS = cycle(COLORS)

# Parameter input:

input_data = ih.cli_input(sys.argv)

if input_data is None:
    input_data = (
        ih.python_input("Width: "),
        ih.python_input("Height: "),
        ih.python_input("Number of lines to draw: ")
    )

width, height, line_count = ih.output_format(input_data)

# Data output template:

data = {
    f"line_{index + 1}": {
        "x": [],
        "y": []
    } for index in range(line_count)
}

# Main loop:

color_cache = []
for index in range(line_count):
    color_cache.append(next(COLORS))

    # Figure setup:

    fig, ax = plt.subplots()
    plt.grid(True)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title(f"Click to add points for line number {index + 1}...")

    # Previous drawings' plotting:

    if index > 0:
        for i in range(index):
            sub_color = color_cache[i]

            if len(data[f"line_{i + 1}"]['x']) > 1:

                coordinates = [
                    Coordinate(x_, y_)
                    for x_, y_ in zip(
                        data[f"line_{i + 1}"]['x'],
                        data[f"line_{i + 1}"]['y']
                    )
                ]

                sp = Spline(
                    coordinates,
                    gen_step=min(width, height) / 1000
                )

                sp.plot_input(
                    INPUT.get("shape"),
                    ms=INPUT.get("size"),
                    alpha=INPUT.get("alpha"),
                    color=f"dark{sub_color}",
                )

                sp.plot_positions(
                    POSITIONS.get("shape"),
                    lw=POSITIONS.get("size"),
                    alpha=POSITIONS.get("alpha"),
                    color=sub_color
                )

    # Line drawing and display:

    line, = ax.plot(
        [], [],
        POSITIONS.get("shape"),
        lw=POSITIONS.get("size") * 2,  # Highlights the line.
        alpha=POSITIONS.get("alpha"),
        color=color_cache[-1]
    )
    builder = LineBuilder(line, ax, width, height, color_cache[-1])

    plt.show()

    # Data storage:

    data[f"line_{index + 1}"]['x'].extend(builder.x)
    data[f"line_{index + 1}"]['y'].extend(builder.y)

# Data output:

with open("coordinates.json", "w", encoding="utf-8") as output:
    json.dump(data, output, ensure_ascii=False, indent=4)
