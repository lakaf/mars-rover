import io
import json
import logging.config
import os
import sys
from typing import List, TextIO

from .constants import COMMAND_LINE_HELP
from .database import RoverMemoryRepo, RoverRepo
from .enums import RoverInputType
from .exceptions import InvalidInputException
from .logging import logging_config
from .parsers import (PlateauInputTextParser, RoverLandingTextParser,
                      RoverMovingTextParser)

logging.config.dictConfig(logging_config)
log = logging.getLogger("marsrover")


def parse_command_line_argv(argv_list: List[str]):
    """Parse user's command line input arguments

    Args:
        argv_list (str): list of input argument strings

    Raises:
        Exception: If arguments length is not 2 or 3

    Returns:
        Tuple[bool, bool]: tuple of 2 bools to indicate
        whether user is in debug mode, and whether user
        is only asking for command line help
    """
    if len(argv_list) < 2 or len(argv_list) > 3:
        print_help = True
        debug_mode = False
    else:
        debug_mode = "--debug" in argv_list
        print_help = "--help" in argv_list

    return debug_mode, print_help


def parse_input(input_file: TextIO, rover_repo: RoverRepo):
    """Main parser for input file.
    It will parse user's input line
    by line.

    Args:
        input_file (TextIO): TextIO object for user's input.
    """
    current_line = 1
    first_line = input_file.readline()

    try:
        # Parse configuration
        plateau = PlateauInputTextParser().parse_input_line(first_line)

        # Parsers for rover input
        # Try to reuse same parser instance instead of creating a new one
        # per input line to save memory usage
        rover_landing_parser = RoverLandingTextParser(plateau, rover_repo)
        rover_moving_parser = RoverMovingTextParser(plateau, rover_repo)

        # Parse rover input
        for line in input_file:
            current_line += 1

            if RoverInputType.LANDING.value in line.upper():
                rover_landing_parser.parse_input_line(line)
            elif RoverInputType.INSTRUCTIONS.value in line.upper():
                rover_moving_parser.parse_input_line(line)

            else:
                raise InvalidInputException(
                    f"Unknown rover input type: {line}")

    except InvalidInputException as invalid_input_ex:
        raise InvalidInputException(
            invalid_input_ex.message, current_line)


# Program main entrance
if __name__ == '__main__':
    try:
        debug_mode, print_help = parse_command_line_argv(sys.argv)

        # Using memory repo in this case
        rover_repo = RoverMemoryRepo()

        if print_help:
            print(COMMAND_LINE_HELP)

        else:
            input_argv = sys.argv[-1]
            if os.path.isfile(input_argv):
                with open(input_argv) as input_file:
                    parse_input(input_file, rover_repo)

            else:
                with io.StringIO(input_argv) as input_io:
                    parse_input(input_io, rover_repo)

            # Outputs report
            rover_repo.report_all_rovers()

    except Exception as ex:
        if debug_mode:
            log.error(ex)
        else:
            log.error("Application exception occurred. "
                      "Please enable debug mode to see more details.")
