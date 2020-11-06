import json
import logging.config
import os
import sys
from typing import List, TextIO

from .constants import COMMAND_LINE_HELP
from .exceptions import InvalidInputException
from .logging import logging_config
from .plateau import Plateau
from .rover import Rover

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
        raise Exception("Invalid argument(s)")

    debug_mode = "--debug" in argv_list
    print_help = "--help" in argv_list

    return debug_mode, print_help


def parse_input(input_file: TextIO):
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
        plateau = Plateau.parse_plateau_input(first_line)

        # Parse rover input
        for line in input_file:
            current_line += 1
            Rover.parse_rover_input(line, plateau)

    except InvalidInputException as invalid_input_ex:
        raise InvalidInputException(
            invalid_input_ex.message, current_line)


# Program main entrance
if __name__ == '__main__':
    try:
        debug_mode, print_help = parse_command_line_argv(sys.argv)

        if print_help:
            print(COMMAND_LINE_HELP)

        else:
            file_path = sys.argv[-1]
            if not os.path.isfile(file_path):
                log.error(
                    f"File {file_path} does not exist, "
                    "please check your input.")
            else:
                with open(file_path) as input_file:
                    parse_input(input_file)

                # Outputs report
                Rover.report_all_rovers()

    except Exception as ex:
        if debug_mode:
            log.error(ex)
        else:
            log.error("Application exception occurred. "
                      "Please enable debug mode to see more details.")
