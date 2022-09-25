"""Simple manual coordinate generator.

Allows the user to generate coordinates by clicking on the matplotlib plot.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


import json
from matplotlib import pyplot as plt


COLORS = [
    "darkorange",
    "darkblue",
    "darkgreen",
    "orange",
    "blue",
    "green"
]


class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect("button_press_event", self)
        self.line.figure.canvas.draw()

    def __call__(self, event):
        print(f"[Event] Type: click - Descriptor: {event}")

        if event.inaxes != self.line.axes:
            return

        self.xs.append(event.xdata)
        self.ys.append(event.ydata)

        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()


if __name__ == "__main__":
    # Input:
    width = float(input("Enter width: "))
    height = float(input("Enter height: "))
    line_no = int(input("Enter the number of lines to draw: "))

    data = {
        f"line_{index + 1}": {
            "x": [],
            "y": []
        } for index in range(line_no)
    }

    for index in range(line_no):
        fig, ax = plt.subplots()
        plt.grid(True)
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_title(f"Click to add points for line number {index + 1}...")

        if index > 0:
            for sub_index in range(index):
                plt.plot(
                    data[f"line_{sub_index + 1}"]['x'],
                    data[f"line_{sub_index + 1}"]['y'],
                    "--",
                    marker="2",
                    markersize=5,
                    color=COLORS[sub_index]
                )

        line, = ax.plot(
            [], [],
            "--",
            marker="2",
            markersize=5,
            color=COLORS[index]
        )

        builder = LineBuilder(line)

        plt.show()

        data[f"line_{index + 1}"]['x'].extend(builder.xs)
        data[f"line_{index + 1}"]['y'].extend(builder.ys)

    with open("coordinates.json", "w", encoding="utf-8") as output:
        json.dump(data, output, ensure_ascii=False, indent=4)
