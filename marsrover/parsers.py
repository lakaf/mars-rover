from abc import ABC, abstractmethod

from .exceptions import InvalidInputException, InvalidRoverOperationException
from .models import Plateau, Rover
from .enums import Orientation
from .util import strip_str_list


class TextParser(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def parse_input_line(self, input_line, *args, **kwargs):
        pass


class PlateauInputTextParser(TextParser):
    def __init__(self):
        super().__init__()

    def parse_input_line(self, input_line: str, *args, **kwargs) -> Plateau:
        """Parser for plateau input.
        Parses user file and returns an plateau instance
        based on input.

        Args:
            input_line (str): Plateau input line

        Raises:
            InvalidInputException: If none or more than 1 colon is found
            InvalidInputException: If coordinates number is not 2
            after the string part following the colon
            InvalidInputException: If input coordinates are not integers
            InvalidInputException: If input coordinates are negative

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
            raise InvalidInputException("Plateau coordinates must be integers")

        if initial_x < 0 or initial_y < 0:
            raise InvalidInputException(
                "Plateau coordinates cannot be negative "
                "integers because lower-left coordinates "
                "are assumed to be 0,0")

        return Plateau(input_parts[0], initial_x, initial_y)


class RoverTextParser(TextParser):
    def __init__(self, plateau: Plateau, rover_repo):
        self._subject_plateau = plateau
        self._rover_repo = rover_repo
        self._acting_rover_name = None
        self._instructions_details = None

    def parse_input_line(self, input_line, *args, **kwargs):
        """Praser for all rover inputs.
        Performs basic validation and extracts
        rover name and instructions for
        further parsing.

        Args:
            input_line (str): Input line from user
            valid sample: "Rover1 Landing:1 2 N"

        Raises:
            InvalidInputException: If none or more than one colon found from input
            InvalidInputException: If none or more than one space found from input header part
        """
        input_parts = input_line.split(":")
        if len(input_parts) != 2:
            raise InvalidInputException("Invalid Rover input")
        input_parts = strip_str_list(input_parts)

        header_parts = input_parts[0].split(" ")
        if len(header_parts) != 2:
            raise InvalidInputException("Invalid Rover input")

        self._acting_rover_name = header_parts[0]
        self._instructions_details = input_parts[1]

    def parser_clean_up(self):
        self._acting_rover_name = None
        self._instructions_details = None


class RoverLandingTextParser(RoverTextParser):
    def __init__(self, plateau, rover_repo):
        super().__init__(plateau, rover_repo)

    def parse_input_line(self, input_line, *args, **kwargs):
        """Parses rover landing inputs.
        Will add newly landed rover to rover registry.

        Args:
            input_line (str): Landing input line from user
            valid sample: "Rover1 Landing:1 2 N"

        Raises:
            InvalidInputException: If landing input format is wrong
            InvalidInputException: If landing coordinates are not numeric
            InvalidInputException: If invalid initial orientation is provided
            InvalidInputException: If target location has already been occupied
        """
        super().parse_input_line(input_line, *args, **kwargs)

        if self._acting_rover_name and self._instructions_details:

            landing_input_parts = self._instructions_details.split(" ")
            if len(landing_input_parts) != 3:
                raise InvalidInputException("Invalid rover landing input")

            if self._rover_repo.get_rover_by_name(self._acting_rover_name):
                raise InvalidInputException(
                    f"Rover {self._acting_rover_name} has already landed before")

            try:
                landing_x = int(landing_input_parts[0])
                landing_y = int(landing_input_parts[1])
            except ValueError:
                raise InvalidInputException(
                    "Invalid rover landing coordinates input: "
                    f"{self._instructions_details}")

            try:
                orientation = Orientation[landing_input_parts[2].upper()]
            except KeyError:
                raise InvalidInputException(
                    f"Invalid rover orientation input: {landing_input_parts[2]}")

            # Check landing collision
            try:
                self._subject_plateau.verify_target_location(
                    landing_x, landing_y)
            except InvalidRoverOperationException:
                raise InvalidInputException(
                    f"Invalid landing location: {landing_x, landing_y}")

            # Add newly landed rover to registry
            self._rover_repo.register_new_rover(self._acting_rover_name, Rover(
                self._subject_plateau, self._acting_rover_name, landing_x,
                landing_y, orientation))

            super().parser_clean_up()


class RoverMovingTextParser(RoverTextParser):
    def __init__(self, plateau, rover_repo):
        super().__init__(plateau, rover_repo)

    def parse_input_line(self, input_line, *args, **kwargs):
        """Parses rover instructions inputs.

        Args:
            rover_name (str): Rover name(also id) to instruct
            instructions_input (str): List of characters instructions
            for specific rover
            valid sample: "Rover2 Instructions:MMRMMRMRRM"

        Raises:
            InvalidInputException: If rover_name does not exist in registry
            InvalidInputException: If an unknown command is passed in
        """
        super().parse_input_line(input_line, *args, **kwargs)

        if self._acting_rover_name and self._instructions_details:
            acting_rover = self._rover_repo.get_rover_by_name(
                self._acting_rover_name)
            if not acting_rover:
                raise InvalidInputException(
                    f"Rover {self._acting_rover_name} does not exist")

            acting_rover.execute_move_commands(self._instructions_details)

            super().parser_clean_up()
