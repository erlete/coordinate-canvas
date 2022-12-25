"""Input handling module.

This module contains all methods needed to handle the input of the package.
It is mean to be used internally by the package and not by the user, since
method implementations are highly specific to the package's needs.

Author:
    Paulo Sanchez (@erlete)
"""


import re


def output_format(values: tuple[str]) -> tuple[float, float, int] | None:
    """Formats the output of the input.

    This method receives a tuple of strings and validates them. If the
    amount of values is less than 3, then a ValueError is raised. If any
    of the values is not a string, then a TypeError is raised. Otherwise,
    the formatted input values are returned.

    The method is meant to be used in combination with the `cli_input`
    and the `python_input` methods.

    Args:
        values (tuple): The input values.

    Raises:
        ValueError: If the input does not have at least 3 values.
        TypeError: If any of the input values is not a string.

    Returns:
        tuple[float, float, int]: The formatted input values.
    """

    if len(values) < 3:
        raise ValueError("the input must have at least 3 values")

    if any(not isinstance(value, str) for value in values):
        raise TypeError("the input values must be strings")

    return (float(values[0]), float(values[1]), int(float(values[2])))


def cli_input(arguments: list[str]) -> tuple[str, str, str] | None:
    """Handles CLI input.

    This class receives a list of arguments and validates them. If the
    amount of arguments is less than 4, then None is returned. If any of
    the arguments is not numeric, then None is returned. Otherwise, the
    raw input values are returned.

    Args:
        arguments (list[str]): The list of arguments from `sys.argv`.

    Returns:
        tuple[str, str, str] | None: The raw input values or None.
    """

    if len(arguments) < 4:
        return None

    values = arguments[1:4]

    if any(not (bool(re.match(r"\d+\.\d+", value))
                or value.isnumeric()) for value in values):

        return None

    return values


def python_input(message: str) -> str:
    """Handles Python input.

    This class receives a message and validates the input. If the input
    is not numeric, then a ValueError is raised. Otherwise, the input is
    returned.

    Args:
        message (str): The message to be displayed to the user.

    Raises:
        ValueError: If the input is not numeric.

    Returns:
        str: The validated input or None.
    """

    value = input(message)

    if not (bool(re.match(r"\d+\.\d+", value)) or value.isnumeric()):
        raise ValueError("the input must be numeric")

    return value
