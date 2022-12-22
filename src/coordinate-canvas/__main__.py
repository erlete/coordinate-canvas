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
from itertools import cycle

import matplotlib.pyplot as plt
from bidimensional import Coordinate
from bidimensional.functions import Spline

from .config import CONFIG
from .utils import LineBuilder


def validate_input(message: str) -> float:
    """Input validation method.

    This method validates a given input. If the input is not numeric, then a
    ValueError is raised.

    Args:
        message (str): The message to be displayed to the user.

    Raises:
        ValueError: If the input is not numeric.

    Returns:
        float: The validated input.
    """

    value = input(message)

    if not value.isnumeric():
        raise ValueError("the input value must be numeric")

    return float(value)


# Constants' definition:

COLORS = cycle(CONFIG.get("colors"))

# Parameter input:

width = validate_input("Enter width: ")
height = validate_input("Enter height: ")
line_count = int(validate_input("Enter the number of lines to draw: "))

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
                CONFIG.get("input").get("shape"),
                ms=CONFIG.get("input").get("size"),
                alpha=CONFIG.get("input").get("alpha"),
                color=f"dark{sub_color}",
            )

            sp.plot_positions(
                CONFIG.get("positions").get("shape"),
                lw=CONFIG.get("positions").get("size"),
                alpha=CONFIG.get("positions").get("alpha"),
                color=sub_color
            )

    # Line drawing and display:

    line, = ax.plot(
        [], [],
        CONFIG.get("positions").get("shape"),
        lw=CONFIG.get("positions").get("size") * 2,  # Highlights the line.
        alpha=CONFIG.get("positions").get("alpha"),
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
