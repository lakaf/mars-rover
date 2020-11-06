import pytest
from marsrover.exceptions import (InvalidInputException,
                                  InvalidRoverOperationException)


def test_invalid_input_exp():
    msg = "Wrong input"
    with pytest.raises(InvalidInputException) as ex:
        raise InvalidInputException(msg, 50)
    assert ex.value.message == msg
    assert ex.value.line_number == 50
    assert str(ex.value) == InvalidInputException.error_template.format(50, msg)

    with pytest.raises(InvalidInputException) as ex:
        raise InvalidInputException(msg)
    assert ex.value.message == msg
    assert ex.value.line_number is None


def test_invalid_cover_op_exp():
    msg = "Wrong operation"
    rover_name = "Rover 777"
    with pytest.raises(InvalidRoverOperationException) as ex:
        raise InvalidRoverOperationException(msg, rover_name)
    assert ex.value.rover_name == rover_name
    assert ex.value.message == msg
    assert str(
        ex.value) == InvalidRoverOperationException.error_template.format(
        rover_name, msg)
