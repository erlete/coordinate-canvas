import json

import matplotlib.pyplot as plt

from .utils import LineBuilder


LINE_COLORS = [
    "darkorange",
    "darkblue",
    "darkgreen",
    "orange",
    "blue",
    "green"
]


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

    # Figure setup:

    fig, ax = plt.subplots()
    plt.grid(True)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title(f"Click to add points for line number {index + 1}...")

    # Previous drawings' plotting:

    if index > 0:
        for sub_index in range(index):

            # Auxiliary index to avoid causing an IndexError:

            color_index = sub_index % len(LINE_COLORS)

            plt.plot(
                data[f"line_{sub_index + 1}"]['x'],
                data[f"line_{sub_index + 1}"]['y'],
                "--",
                marker="2",
                markersize=5,
                color=LINE_COLORS[color_index]
            )

    # Line drawing and display:

    line, = ax.plot(
        [], [],
        "--",
        marker="2",
        markersize=5,
        color=LINE_COLORS[index]
    )
    builder = LineBuilder(line)
    plt.show()

    # Data storage:

    data[f"line_{index + 1}"]['x'].extend(builder.x)
    data[f"line_{index + 1}"]['y'].extend(builder.y)

# Data output:

with open("coordinates.json", "w", encoding="utf-8") as output:
    json.dump(data, output, ensure_ascii=False, indent=4)
