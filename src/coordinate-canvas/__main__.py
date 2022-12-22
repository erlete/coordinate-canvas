import json

import matplotlib.pyplot as plt

from .utils import LineBuilder
from bidimensional import Coordinate
from bidimensional.functions import Spline
from itertools import cycle

import json
from .config import CONFIG


COLORS = cycle(CONFIG.get("colors"))
colorcache = []

# Parameter input:

width = float(input("Enter width: "))
height = float(input("Enter height: "))
line_no = int(input("Enter the number of lines to draw: "))

# Data output template:

data = {
    f"line_{index + 1}": {
        "x": [],
        "y": []
    } for index in range(line_no)
}

for index in range(line_no):
    colorcache.append(next(COLORS))
    # Figure setup:

    fig, ax = plt.subplots()
    plt.grid(True)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title(f"Click to add points for line number {index + 1}...")

    # Previous drawings' plotting:

    if index > 0:
        for sub_index in range(index):
            sub_color = colorcache[sub_index]

            coordinates = [
                Coordinate(x_, y_)
                for x_, y_ in zip(
                    data[f"line_{sub_index + 1}"]['x'],
                    data[f"line_{sub_index + 1}"]['y']
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
        "-",
        color=colorcache[-1]
    )
    builder = LineBuilder(line, ax, width, height, colorcache[-1])
    plt.show()

    # Data storage:

    data[f"line_{index + 1}"]['x'].extend(builder.x)
    data[f"line_{index + 1}"]['y'].extend(builder.y)

# Data output:

with open("coordinates.json", "w", encoding="utf-8") as output:
    json.dump(data, output, ensure_ascii=False, indent=4)
