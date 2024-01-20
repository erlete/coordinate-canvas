"""Configuration module.

Author:
    Paulo Sanchez (@erlete)
"""


class Point:
    """Plot point configuration.

    Attributes:
        SHAPE (str): point shape.
        SIZE (int | float): point size.
        ALPHA (int | float): point alpha.
    """

    SHAPE = "o"
    SIZE = 5
    ALPHA = 1


class Link:
    """Plot link configuration.

    Attributes:
        SHAPE (str): link shape.
        SIZE (int | float): link size.
        ALPHA (int | float): link alpha.
    """

    SHAPE = "-"
    SIZE = 1
    ALPHA = 0.5


class CLI:
    """CLI commands configuration.

    Attributes:
        WIDTH (int): canvas width.
        HEIGHT (int): canvas height.
        OUTPUT (str): output file path.
    """

    WIDTH = 10
    HEIGHT = 10
    OUTPUT = "coordinates.json"
