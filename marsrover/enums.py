"""Module for enum classes"""

from enum import Enum, unique


class Orientation(Enum):
    """Enum class for rover orientation.
    Value represents x y ratio on movement.
    """
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)
    N = (0, 1)


class RoverInputType(Enum):
    """Enum class for rover input type.
    """
    LANDING = "LANDING"
    INSTRUCTIONS = "INSTRUCTIONS"
