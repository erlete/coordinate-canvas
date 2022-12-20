"""Simple manual coordinate generator.

Allows the user to generate coordinates by clicking on the matplotlib plot.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


from matplotlib import pyplot as plt


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
