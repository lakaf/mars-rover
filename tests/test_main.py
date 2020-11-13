import io

import marsrover.__main__
import pytest
from marsrover.exceptions import InvalidInputException
from marsrover.database import RoverMemoryRepo


@pytest.fixture()
def rover_repo():
    return RoverMemoryRepo()


@pytest.fixture()
def test_input_file_io():
    test_input = [
        'Plateau:5 5',
        'Rover1 Landing:1 2 N',
        'Rover1 Instructions:LMLMLMLMM',
        'Rover2 Landing:3 3 E',
        'Rover2 Instructions:MMRMMRMRRM'
    ]
    stream = io.StringIO('\n'.join(test_input))

    return stream


@pytest.fixture()
def test_input_file_io_unknown():
    test_input = [
        'Plateau:5 5',
        'Rover1 Restart:1 2 N',
        'Rover1 Instructions:LMLMLMLMM',
        'Rover2 Landing:3 3 E',
        'Rover2 Instructions:MMRMMRMRRM'
    ]
    stream = io.StringIO('\n'.join(test_input))

    return stream


@pytest.fixture()
def test_input_file_io_invalid_input():
    test_input = [
        'Plateau:5 5',
        'Plateau:5 5',
    ]
    stream = io.StringIO('\n'.join(test_input))
    return stream


def test_parse_command_line_argv():
    assert (False, True) == marsrover.__main__.parse_command_line_argv([])
    assert (False, True) == marsrover.__main__.parse_command_line_argv(['a'])
    assert(
        False, True) == marsrover.__main__.parse_command_line_argv(
        ['a', 'b', 'c', 'd'])

    assert(
        False, False) == marsrover.__main__.parse_command_line_argv(
        ['app', 'input'])
    assert(
        True, False) == marsrover.__main__.parse_command_line_argv(
        ['app', '--debug'])
    assert(
        True, False) == marsrover.__main__.parse_command_line_argv(
        ['app', '--debug', 'input'])
    assert(
        False, True) == marsrover.__main__.parse_command_line_argv(
        ['app', '--help'])
    assert(
        True, True) == marsrover.__main__.parse_command_line_argv(
        ['app', '--debug', '--help'])


def test_parse_input(test_input_file_io, rover_repo):
    marsrover.__main__.parse_input(test_input_file_io, rover_repo)


def test_invalid_input_exception_with_line(
        test_input_file_io_invalid_input, rover_repo):
    with pytest.raises(InvalidInputException) as ex:
        marsrover.__main__.parse_input(
            test_input_file_io_invalid_input, rover_repo)

    # Bad input is on line 2
    assert ex.value.line_number == 2


def test_unknown_input_type(test_input_file_io_unknown, rover_repo):
    expected_msg = "Unknown rover input type: {}"
    with pytest.raises(InvalidInputException) as ex:
        marsrover.__main__.parse_input(test_input_file_io_unknown, rover_repo)
    assert ex.value.message == expected_msg.format("Rover1 Restart:1 2 N\n")
