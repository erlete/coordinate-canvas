import json
import os

import regex as re
from colorama import Fore, Style


class InputFileHandler:
    """Input file handler class.

    This class is responsible for receiving the path to an input file, as well
    as checking its existence, extension and structure.

    Attributes:
        path (str): input file path.
        EXTENSIONS (tuple[str]): sequence of supported file extensions
            (lowercase with no dots).
    """

    EXTENSIONS: tuple[str] = (
        "json",
    )

    def __init__(self, path: str) -> None:
        """Initialize an InputFileHandler instance.

        This method also tests the input file existence, extension and
        structure automatically.

        Args:
            path (str): input file path.
        """
        self.path = path

        # File checks' execution:
        self._check_file_exists()
        self._check_file_extension()
        self._check_file_structure()

    @property
    def path(self) -> str:
        """Get input file path.

        Returns:
            str: input file path.
        """
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        """Set input file path.

        Args:
            path (str): input file path.
        """
        if not isinstance(path, str):
            raise TypeError("input file path must be a string")

        self._path = path

    def _check_file_exists(self) -> None:
        """Check if input file exists.

        Raises:
            FileNotFoundError: if input file does not exist.
        """
        if not os.path.exists(self._path):
            raise FileNotFoundError(
                f"input file \"{self._path}\" does not exist"
            )

    def _check_file_extension(self) -> None:
        """Check file extension format.

        Raises:
            TypeError: if input file has got the incorrect format.
        """
        if not self._path.strip().split(".")[-1].lower() in self.EXTENSIONS:
            raise TypeError(
                "input file must be one of the following formats: "
                + ", ".join(self.EXTENSIONS)
            )

    def _check_file_structure(self) -> None:
        """Check if input file has the correct structure.

        Raises:
            ValueError: if input file does not have the correct structure.
        """
        with open(self._path, mode="r", encoding="utf-8") as fp:
            data = json.load(fp)

        try:
            assert isinstance(data, dict)
            assert all(isinstance(key, str) for key in data.keys())
            assert all(
                re.match(r"^line_\d{1}$", key) is not None
                for key in data.keys()
            )
            assert all(isinstance(value, dict) for value in data.values())
            assert all(
                tuple(value.keys()) == ("x", "y")
                for value in data.values()
            )
            assert all(
                isinstance(sub_value, list)
                for value in data.values()
                for sub_value in value.values()
            )
            assert all(
                isinstance(coordinate, float)
                for value in data.values()
                for sub_value in value.values()
                for coordinate in sub_value
                # I know this is complex as hell. Not gonna change it, though.
            )

        except AssertionError:
            print(
                Fore.RED + Style.BRIGHT
                + "[Error] Invalid input file format. Aborting..."
                + Style.RESET_ALL
            )
            exit(1)
