"""Module to handle logic about plateau"""
from typing import Tuple

from .enums import Orientation, RoverInputType
from .exceptions import InvalidInputException, InvalidRoverOperationException
from .util import strip_str_list


class Plateau:
    def __init__(self, name: str, max_x: int, max_y: int):
        self._name = name
        self._max_x = max_x
        self._max_y = max_y
        self._occupied_locations = {}

    @property
    def name(self):
        return self._name

    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y

    def verify_target_location(self, x: int, y: int):
        if x < 0:
            raise InvalidRoverOperationException(
                "Crossing left border")

        if x > self.max_x:
            raise InvalidRoverOperationException(
                "Crossing right border")

        if y < 0:
            raise InvalidRoverOperationException(
                "Crossing lower border")

        if y > self.max_y:
            raise InvalidRoverOperationException(
                "Crossing upper border")

        if (x, y) in self._occupied_locations:
            raise InvalidRoverOperationException(
                "Collision detected")

    def update_occupied_location(
            self, moved_rover, previous_rover_location: Tuple[int, int] = None):
        if (previous_rover_location and previous_rover_location in self._occupied_locations):
            del self._occupied_locations[previous_rover_location]

        self._occupied_locations[(
            moved_rover.current_x, moved_rover.current_y)] = moved_rover


class Rover:
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
        self._current_x = value

    @property
    def current_y(self):
        return self._current_y

    @current_y.setter
    def current_y(self, value):
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
        proposed_x = self.current_x + self.current_orientation.value[0]
        proposed_y = self.current_y + self.current_orientation.value[1]

        try:
            self.plateau.verify_target_location(proposed_x, proposed_y)
            self.current_x = proposed_x
            self.current_y = proposed_y

        except InvalidRoverOperationException as ex:
            # Raise up with rover name
            raise InvalidRoverOperationException(
                ex.message, self.name)

    def execute_move_commands(self, commands: str):
        """Executes a series of movement command characters.
        Updates rover's location in corresopnding plateau after.

        Args:
            commands (str): Input strong consists of a series
            of character commands
        """
        original_location = (self.current_x, self.current_y)
        for command in commands:
            self.execute_single_move_command(command)

        self.update_location_on_plateau(original_location)

    def execute_single_move_command(self, command_char):
        """Executes a single command.

        Args:
            command_char (str): A digit string, will be used
            to look for corresponding command from registry

        Raises:
            InvalidInputException: If requested command is 
            not found in command registry
        """
        if command_char not in self.__class__.commands_registry:
            raise InvalidInputException(
                f"Unknown rover instruction: {command_char}")

        # Executes command
        getattr(self, self.__class__.commands_registry[command_char])()

    def report_status(self) -> str:
        """Reports current status of a rover.

        Returns:
            str: String to represents a rover's current status
        """
        return (
            f"{self.name}:{self.current_x} "
            f"{self.current_y} {self.current_orientation.name}")

    def update_location_on_plateau(self, original_location: Tuple[int, int]):
        """Updates plateau's map after movements have been done.

        Args:
            original_location (Tuple[int, int]): Original location
            of the rover before it moves
        """
        self.plateau.update_occupied_location(self, original_location)
