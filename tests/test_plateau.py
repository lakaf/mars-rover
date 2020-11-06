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


def test_parser_wrong_input():
    expected_error_message = "Invalid configuration input format"
    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("ABCDEFG!~@#%^")
    assert ex.value.message == expected_error_message

    with pytest.raises(InvalidInputException) as ex:
        Plateau.parse_plateau_input("hello:world:peace")
    assert ex.value.message == expected_error_message
