import io

import marsrover.__main__
import pytest
from marsrover.exceptions import InvalidInputException


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


def test_parse_input(test_input_file_io):
    marsrover.__main__.parse_input(test_input_file_io)


def test_invalid_input_exception_with_line(test_input_file_io_invalid_input):
    with pytest.raises(InvalidInputException) as ex:
        marsrover.__main__.parse_input(test_input_file_io_invalid_input)

    # Bad input is on line 2
    assert ex.value.line_number == 2
