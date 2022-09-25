"""Simple manual coordinate generator.

Allows the user to generate coordinates by clicking on the matplotlib plot.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


import json
from matplotlib import pyplot as plt


    "darkorange",
    "darkblue",
    "darkgreen",
    "orange",
    "blue",
    "green"
]


class LineBuilder:
    """Builds a line based on click event handlers.

    This class is used to build a line based on click events. The line is
    built by clicking on the matplotlib plot. The coordinates are stored
    in a list of tuples.
    """

    def __init__(self, line):
        self.line = line
        self.x, self.y = list(line.get_xdata()), list(line.get_ydata())

        self.cid = line.figure.canvas.mpl_connect("button_press_event", self)
        self.line.figure.canvas.draw()

    def __call__(self, event):
        if event.inaxes != self.line.axes:
            return

        self.x.append(event.xdata)
        self.y.append(event.ydata)

        self.line.set_data(self.x, self.y)
        self.line.figure.canvas.draw()


if __name__ == "__main__":

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
                plt.plot(
                    data[f"line_{sub_index + 1}"]['x'],
                    data[f"line_{sub_index + 1}"]['y'],
                    "--",
                    marker="2",
                    markersize=5,
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
