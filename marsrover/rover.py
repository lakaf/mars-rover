"""Module to handle rover logic"""

from .enums import Orientation, RoverInputType
from .exceptions import InvalidInputException, InvalidRoverOperationException
from .plateau import Plateau
from .util import strip_str_list


class Rover:
    rover_registry = {}

    commands_registry = {
        'L': "turn_left",
        'R': "turn_right",
        'M': "move_forward"
    }

    # Works as a circular list for turning
    orientations = [
        Orientation.E,
        Orientation.S,
        Orientation.W,
        Orientation.N,
    ]

    def __init__(self, plateau: Plateau, name: str, current_x: int,
                 current_y: int, current_orientation: Orientation):
        self._plateau = plateau
        self._name = name
        self._current_orientation = current_orientation

        # Set through setters
        self.current_x = current_x
        self.current_y = current_y

    @property
    def plateau(self):
        return self._plateau

    @property
    def name(self):
        return self._name

    @property
    def current_x(self):
        return self._current_x

    @current_x.setter
    def current_x(self, value):
        if value > self.plateau.max_x:
            raise InvalidRoverOperationException(
                "Crossing right border", self.name)

        elif value < 0:
            raise InvalidRoverOperationException(
                "Crossing left border", self.name)

        self._current_x = value

    @property
    def current_y(self):
        return self._current_y

    @current_y.setter
    def current_y(self, value):
        if value > self.plateau.max_y:
            raise InvalidRoverOperationException(
                "Crossing upper border", self.name)

        elif value < 0:
            raise InvalidRoverOperationException(
                "Crossing lower border", self.name)

        self._current_y = value

    @property
    def current_orientation(self):
        return self._current_orientation

    def turn_left(self):
        """Let rover do a left turn (counter-clockwise).
        """
        # Move 1 step left in circular list
        self._current_orientation = self.__class__.orientations[
            (self.__class__.orientations.index(self.current_orientation)
             - 1) % len(self.__class__.orientations)]

    def turn_right(self):
        """Let rover do a right turn (clockwise).
        """
        # Move 1 step right in circular list
        self._current_orientation = self.__class__.orientations[
            (self.__class__.orientations.index(self.current_orientation)
             + 1) % len(self.__class__.orientations)]

    def move_forward(self):
        """Modifies x or y based on orientation.
        """
        self.current_x = self.current_x + self.current_orientation.value[0]
        self.current_y = self.current_y + self.current_orientation.value[1]

    def report_status(self) -> str:
        """Reports current status of a rover.

        Returns:
            str: String to represents a rover's current status
        """
        return (
            f"{self.name}:{self.current_x} "
            f"{self.current_y} {self.current_orientation.name}")

    @classmethod
    def register_new_rover(cls, rover_name: str, rover_obj: 'Rover'):
        """Registers a new rover into registry.
        It will overwrite if an existing name is
        provided.

        Args:
            rover_name (str): Name of the new rover, will be used
            as ID (key) in registry
            rover_obj (Rover): New rover obj reference
        """
        cls.rover_registry[rover_name] = rover_obj

    @classmethod
    def get_rover_by_name(cls, rover_name: str) -> 'Rover':
        """Fetches a rover from registry by its name

        Returns:
            Rover: Rover object with provided name,
            None if the provided name cannot be found
        """
        return cls.rover_registry.get(rover_name)

    @classmethod
    def parse_rover_input(cls, input_line: str, plateau: Plateau):
        """Praser for all rover inputs.
        Performs basic validation and deligate
        to more specific parsers.

        Args:
            input_line (str): Input line from user
            valid sample: "Rover1 Landing:1 2 N"
            plateau (Plateau): Plateau obj where rover
            has landed on

        Raises:
            InvalidInputException: If none or more than one colon found from input
            InvalidInputException: If none or more than one space found from input header part
            InvalidInputException: If unknown input type is found (not
            defined in enum RoverInputType)
        """
        input_parts = input_line.split(":")
        if len(input_parts) != 2:
            raise InvalidInputException("Invalid Rover input")
        input_parts = strip_str_list(input_parts)

        header_parts = input_parts[0].split(" ")
        if len(header_parts) != 2:
            raise InvalidInputException("Invalid Rover input")

        if header_parts[1].upper() == RoverInputType.LANDING.value:
            cls.parse_landing(header_parts[0], input_parts[1], plateau)
        elif header_parts[1].upper() == RoverInputType.INSTRUCTIONS.value:
            cls.parse_instructions(header_parts[0], input_parts[1])
        else:
            raise InvalidInputException(
                f"Unknown rover input type: {header_parts[1]}")

    @classmethod
    def parse_landing(cls, rover_name: str, landing_input: str,
                      plateau: Plateau):
        """Parses rover landing inputs.
        Will add newly landed rover to rover registry.

        Args:
            rover_name (str): Name of the newly landing rover,
            will be used as a rover's id in registry
            landing_input (str): Input to indicate initial X and Y
            coordinates and orientation of a newly landing rover
            valid sample: "1 2 N"
            plateau (Plateau): The plateau object which will
            limit the rover's moving borders

        Raises:
            InvalidInputException: If landing input format is wrong
            InvalidInputException: If landing coordinates are not numeric
            InvalidInputException: If invalid initial orientation is provided
        """
        landing_input_parts = landing_input.split(" ")
        if len(landing_input_parts) != 3:
            raise InvalidInputException("Invalid rover landing input")

        if cls.get_rover_by_name(rover_name):
            raise InvalidInputException(
                f"Rover {rover_name} has already landed before")

        try:
            landing_x = int(landing_input_parts[0])
            landing_y = int(landing_input_parts[1])
        except ValueError:
            raise InvalidInputException(
                f"Invalid rover landing coordinates input: {landing_input}")

        try:
            orientation = Orientation[landing_input_parts[2].upper()]
        except KeyError:
            raise InvalidInputException(
                f"Invalid rover orientation input: {landing_input_parts[2]}")

        # Add newly landed rover to registry
        cls.register_new_rover(rover_name, Rover(
            plateau, rover_name, landing_x,
            landing_y, orientation))

    @classmethod
    def parse_instructions(cls, rover_name: str, instructions_input: str):
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
        acting_rover = cls.get_rover_by_name(rover_name)
        if not acting_rover:
            raise InvalidInputException(f"Rover {rover_name} does not exist")

        for command in instructions_input:
            if command not in cls.commands_registry:
                raise InvalidInputException(
                    f"Unknown rover instruction: {command}")

            # Executes command
            getattr(acting_rover, cls.commands_registry[command])()

    @classmethod
    def report_all_rovers(cls):
        """Reports status of all registered rovers.
        """
        for rover in cls.rover_registry.values():
            print(rover.report_status())
