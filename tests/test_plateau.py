import pytest
from marsrover.exceptions import InvalidInputException, InvalidRoverOperationException
from marsrover.models import Plateau, Rover
from marsrover.parsers import PlateauInputTextParser
from marsrover.enums import Orientation


@pytest.fixture()
def plateau_parser():
    return PlateauInputTextParser()


@pytest.fixture()
def basic_plateau():
    return Plateau("Test Plateau", 10, 10)


@pytest.fixture()
def rover_middle(basic_plateau):
    return Rover(basic_plateau, "Testing landing", 5, 5, Orientation.N)


def test_plateau_properties(basic_plateau):
    assert basic_plateau.name == "Test Plateau"
    assert basic_plateau.max_x == 10
    assert basic_plateau.max_y == 10


def test_parser_base(plateau_parser):
    good_input = "Plateau:5 5"
    plateau = plateau_parser.parse_input_line(good_input)
    assert plateau.name == "Plateau"
    assert plateau.max_x == 5
    assert plateau.max_y == 5

    good_input_dot = "Plateau:0 0"
    plateau = plateau_parser.parse_input_line(good_input_dot)
    assert plateau.name == "Plateau"
    assert plateau.max_x == 0
    assert plateau.max_y == 0

    good_input_line = "Plateau:0 10"
    plateau = plateau_parser.parse_input_line(good_input_line)
    assert plateau.name == "Plateau"
    assert plateau.max_x == 0
    assert plateau.max_y == 10


def test_parser_wrong_input(plateau_parser):
    expected_error_message = "Invalid configuration input format"
    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("ABCDEFG!~@#%^")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("hello:world:peace")
    assert ex.value.message == expected_error_message


def test_parser_wrong_coor_input(plateau_parser):
    expected_error_message = "Invalid coordinates format in configuration input"
    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("Some name: 1    2 3")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("Some name: 1  2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("Some name:")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("Some name:1")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("Some name:     ")
    assert ex.value.message == expected_error_message


def test_paser_non_int_coor(plateau_parser):
    expected_error_message = "Plateau coordinates must be integers"
    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("ABCDEFG:1.3 2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("ABCDEFG:1 2.0")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("ABCDEFG:1.23 2.0")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("ABCDEFG:A 2.0")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("ABCDEFG:? 2.0")
    assert ex.value.message == expected_error_message


def test_parser_negative_coor(plateau_parser):
    expected_error_message = (
        "Plateau coordinates cannot be negative "
        "integers because lower-left coordinates "
        "are assumed to be 0,0")

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("???:-1 2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("???:1 -2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        plateau_parser.parse_input_line("???:-3 -2")
    assert ex.value.message == expected_error_message


def test_landing_rover(basic_plateau, rover_middle):
    basic_plateau.update_occupied_location(rover_middle)
    with pytest.raises(InvalidRoverOperationException) as ex:
        assert basic_plateau.verify_target_location(5, 5)
