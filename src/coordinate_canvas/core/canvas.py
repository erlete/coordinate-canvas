import json
from typing import Any


class Canvas:

    def __init__(self, width: int | float, height: int | float, line_count: int):
        self.width = width
        self.height = height
        self.line_count = line_count
        self.lines = []
        self.current_data = [None, 0]
        self.colors = cycle(COLORS)
        self.ax = plt.gca()
        self.fig = plt.gcf()

        self.fig.canvas.mpl_connect("key_press_event", self.decide)
        self.fig.canvas.mpl_connect("key_release_event", self.exit)

        plt.grid(True)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)

    def decide(self, event):
        if event.key.isnumeric() and 1 <= int(event.key) <= self.line_count:
            self.lines[self.current_data[1]].get("line_builder").disconnect()
            self.lines[int(event.key) - 1].get("line_builder").connect()

            self.current_data[0] = self.lines[int(event.key) - 1].get("line")
            self.current_data[1] = int(event.key) - 1

            self.fig.suptitle(
                f"Click to add points for line number {self.current_data[1] + 1}...",
                fontsize="large", fontweight="bold"
            )

    def save(self, event):
        if event.key == "s":
            with open("data.json", "w") as file:
                json.dump(self.lines, file, indent=4)

    def exit(self, event: Any) -> None:
        """Canvas exit handler.

        This method handles the exit event of the canvas. It is called when the
        user presses the escape key or the q key. It saves the data to a JSON
        file and exits the program.

        Args:
            event (Any): The event object.
        """
        if event.key in ("escape", "q"):
            # TODO: Implement saving logic here.
            exit(0)
