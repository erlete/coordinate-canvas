"""CLI module.

Author:
    Paulo Sanchez (@erlete)
"""


import click

from .. import config as cfg


@click.command("coordinate-canvas")
@click.option(
    "--width",
    "-w",
    default=cfg.CLI.WIDTH,
    show_default=True,
    type=click.FloatRange(min=1, max_open=True),
    help="Width of the canvas"
)
@click.option(
    "--height",
    "-h",
    default=cfg.CLI.HEIGHT,
    show_default=True,
    type=click.FloatRange(min=1, max_open=True),
    help="Height of the canvas"
)
@click.option(
    "--output",
    "-o",
    default=cfg.CLI.OUTPUT,
    show_default=True,
    type=click.Path(exists=False, dir_okay=False, writable=True),
    help="Output file path"
)
@click.argument(
    "line-count",
    type=click.IntRange(min=1, max=9)
)
def cli(width, height, output, line_count):
    """Plot a canvas for coordinate drawing

    This command allows the user to plot a canvas of a given width and height
    to draw coordinates on it. The user can also specify the number of lines
    to draw on the canvas. Usage information is available on the plot itself.
    """
    # Output file format check:
    if not output.lower().endswith(".json"):
        raise click.BadParameter("Output file must be a JSON file")

    pass  # TODO: Implement core logic here.
