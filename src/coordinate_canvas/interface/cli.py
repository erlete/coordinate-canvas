import click

# Defaults:
WIDTH = 10  # [m]
HEIGHT = WIDTH  # [m]
LINES = 2


@click.command("coordinate-canvas")
@click.option(
    "--width",
    "-w",
    default=WIDTH,
    show_default=True,
    type=click.FloatRange(min=1, max_open=True),
    help="Width of the canvas"
)
@click.option(
    "--height",
    "-h",
    default=HEIGHT,
    show_default=True,
    type=click.FloatRange(min=1, max_open=True),
    help="Height of the canvas"
)
@click.argument(
    "line-count",
    type=click.IntRange(min=1, max=9)
)
def cli(width, height, lines):
    """Plot a canvas for coordinate drawing

    This command allows the user to plot a canvas of a given width and height
    to draw coordinates on it. The user can also specify the number of lines
    to draw on the canvas. Usage information is available on the plot itself.
    """
    pass  # TODO: Implement core logic here.
