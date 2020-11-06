"""Module to handle logic about plateau"""
from .exceptions import InvalidInputException
from .util import strip_str_list


class Plateau:
    def __init__(self, name: str, max_x: int, max_y: int):
        self._name = name
        self._max_x = max_x
        self._max_y = max_y

    @property
    def name(self):
        return self._name

    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y

    @classmethod
    def parse_plateau_input(cls, input_line: str):
        """Parser for plateau input.
        Parses user file and returns an plateau instance
        based on input.

        Args:
            input_line (str): Plateau input line

        Raises:
            InvalidInputException: If none or more than 1 colon is found
            InvalidInputException: If none or more than 1 space is found
            after the string part following the colon
            InvalidInputException: If input coordinates are not integers

        Returns:
            Plateau: Plateau object based on user input
        """
        input_parts = input_line.split(":")
        if len(input_parts) != 2:
            raise InvalidInputException("Invalid configuration input format")
        input_parts = strip_str_list(input_parts)

        coordinates = input_parts[1].split(" ")
        if len(coordinates) != 2:
            raise InvalidInputException(
                f"Invalid coordinates format in configuration input")

        try:
            initial_x = int(coordinates[0])
            initial_y = int(coordinates[1])
        except ValueError:
            raise InvalidInputException(f"Coordinates must be integers")

        return Plateau(input_parts[0], initial_x, initial_y)
