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
AX = plt.gca()
FIG = plt.gcf()


# Methods' definition:

def decide(event):

    if event.key.isnumeric() and 0 <= int(event.key) < LINE_COUNT:
        lines[current_data[1]].get("line_builder").disconnect()
        lines[int(event.key)].get("line_builder").connect()

        current_data[0] = lines[int(event.key)].get("line")
        current_data[1] = int(event.key)

        AX.set_title(f"Click to add points for line number {current_data[1]}...")


def close(event):
    if event.key == "escape":
        exit(0)


# Parameter input:

input_data = ih.cli_input(sys.argv)

if input_data is None:
    input_data = (
        ih.python_input("Width: "),
        ih.python_input("Height: "),
        ih.python_input("Number of lines to draw: ")
    )

width, height, line_count = ih.output_format(input_data)
FIG.canvas.mpl_connect("key_press_event", decide)
FIG.canvas.mpl_connect("key_release_event", close)

# Data output template:

data = {
    f"line_{index + 1}": {
        "x": [],
        "y": []
    } for index in range(line_count)
}

lines = [
    {
        "color": (color := next(COLORS)),
        "line": (line := AX.plot(
            [], [],
            POSITIONS.get("shape"),
            lw=POSITIONS.get("size"),
            alpha=POSITIONS.get("alpha"),
            color=color
        )[0]),
        "line_builder": LineBuilder(line, AX, width, height, color)
    }
    for _ in range(line_count)
]

# Initial connection and setting:

current_data = [lines[0].get("line"), 0]
lines[0].get("line_builder").connect()
AX.set_title("Click to add points for line number 0...")


line, index = current_data
builder = lines[index].get("line_builder")


plt.grid(True)
AX.set_xlim(0, width)
AX.set_ylim(0, height)

plt.show()

# Data storage:

for index in range(line_count):
    data[f"line_{index + 1}"]['x'].extend(lines[index].get("line_builder").x)
    data[f"line_{index + 1}"]['y'].extend(lines[index].get("line_builder").y)

# Data output:

with open("coordinates.json", "w", encoding="utf-8") as output:
    json.dump(data, output, ensure_ascii=False, indent=4)
