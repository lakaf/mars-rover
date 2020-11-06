import pytest
from marsrover.exceptions import InvalidInputException
from marsrover.plateau import Plateau


@pytest.fixture()
def basic_plateau():
    return Plateau("Test Plateau", 10, 10)


def test_plateau_properties(basic_plateau):
    assert basic_plateau.name == "Test Plateau"
    assert basic_plateau.max_x == 10
    assert basic_plateau.max_y == 10


def test_parser_base():
    good_input = "Plateau:5 5"
    plateau = Plateau.parse_plateau_input(good_input)
    assert plateau.name == "Plateau"
    assert plateau.max_x == 5
    assert plateau.max_y == 5

    good_input_dot = "Plateau:0 0"
    plateau = Plateau.parse_plateau_input(good_input_dot)
    assert plateau.name == "Plateau"
    assert plateau.max_x == 0
    assert plateau.max_y == 0

    good_input_line = "Plateau:0 10"
    plateau = Plateau.parse_plateau_input(good_input_line)
    assert plateau.name == "Plateau"
    assert plateau.max_x == 0
    assert plateau.max_y == 10


def test_parser_wrong_input():
    expected_error_message = "Invalid configuration input format"
    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("ABCDEFG!~@#%^")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("hello:world:peace")
    assert ex.value.message == expected_error_message


def test_parser_wrong_coor_input():
    expected_error_message = "Invalid coordinates format in configuration input"
    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("Some name: 1    2 3")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("Some name: 1  2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("Some name:")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("Some name:1")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("Some name:     ")
    assert ex.value.message == expected_error_message


def test_paser_non_int_coor():
    expected_error_message = "Plateau coordinates must be integers"
    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("ABCDEFG:1.3 2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("ABCDEFG:1 2.0")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("ABCDEFG:1.23 2.0")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("ABCDEFG:A 2.0")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("ABCDEFG:? 2.0")
    assert ex.value.message == expected_error_message


def test_parser_negative_coor():
    expected_error_message = (
        "Plateau coordinates cannot be negative "
        "integers because lower-left coordinates "
        "are assumed to be 0,0")

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("???:-1 2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("???:1 -2")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("???:-3 -2")
    assert ex.value.message == expected_error_message
