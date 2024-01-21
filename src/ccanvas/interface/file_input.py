import json
import os
from abc import ABCMeta, abstractmethod

import regex as re
from colorama import Fore, Style


class FileHandler(metaclass=ABCMeta):
    """Abstract file handler class.

    Attributes:
        path (str): file path.
        VALID_EXTENSIONS (tuple[str]): sequence of supported file extensions
            (lowercase with no dots).
    """

    VALID_EXTENSIONS: tuple[str] = ("",)

    def __init__(self, path: str) -> None:
        """Initialize FileHandler instance.

        Args:
            path (str): file path.
        """
        self.path = path

    @property
    def path(self) -> str:
        """Get file path.

        Returns:
            str: file path.
        """
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        """Set file path.

        Args:
            path (str): file path.
        """
        if not isinstance(path, str):
            raise TypeError("file path must be a string")

        self._path = path

    def validate(self) -> None:
        """Determine whether the file is valid or not.

        This method is responsible for executing all the pertinent checks to
        determine whether the file is valid or not.

        Raises:
            FileNotFoundError: if file does not exist.
            TypeError: if file has got the incorrect format.
            ValueError: if file does not have the correct structure.
        """
        self.validate_existence()
        self.validate_extension()
        self.validate_structure()

    def validate_existence(self) -> None:
        """Check if file exists.

        Raises:
            FileNotFoundError: if file does not exist.
        """
        if not os.path.exists(self._path):
            raise FileNotFoundError(f"file \"{self._path}\" does not exist")

    def validate_extension(self) -> None:
        """Check file extension format.

        Raises:
            TypeError: if file has got the incorrect format.
        """
        name = self._path.strip().split(".")[-1].lower()

        if not name in self.VALID_EXTENSIONS:
            raise TypeError(
                f"file must contain one of the following extensions: "
                + ", ".join(self.VALID_EXTENSIONS)
            )

    @abstractmethod
    def validate_structure(self) -> None:
        """Check if file has the correct structure.

        Raises:
            ValueError: if file does not have the correct structure.
        """
        pass


class InputFileHandler(FileHandler):
    """Input file handler class.

    This class is responsible for receiving the path to an input file, as well
    as checking its existence, extension and structure.

    Attributes:
        path (str): input file path.
        VALID_EXTENSIONS (tuple[str]): sequence of supported file extensions
            (lowercase with no dots).
    """

    VALID_EXTENSIONS: tuple[str] = ("json",)

    def validate_structure(self) -> None:
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
