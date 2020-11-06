import pytest
from marsrover.enums import Orientation
from marsrover.exceptions import (InvalidInputException,
                                  InvalidRoverOperationException)
from marsrover.plateau import Plateau
from marsrover.rover import Rover


@pytest.fixture()
def square_plataeu():
    return Plateau("Plateau", 5, 5)


@pytest.fixture()
def dot_plataeu():
    return Plateau("Plateau", 0, 0)


@pytest.fixture()
def rover_at_middle(square_plataeu):
    return Rover(
        square_plataeu,
        "Rover Middle",
        3, 3, Orientation.N
    )


@pytest.fixture()
def rover_at_edge(square_plataeu):
    return Rover(
        square_plataeu,
        "Rover Edge",
        0, 0, Orientation.S
    )


@pytest.fixture()
def rover_at_dot(dot_plataeu):
    return Rover(
        dot_plataeu,
        "Rover Dot",
        0, 0, Orientation.N
    )


@pytest.fixture()
def rover_registry(rover_at_middle, rover_at_edge):
    return {
        rover_at_middle.name: rover_at_middle,
        rover_at_edge.name: rover_at_edge
    }


def test_rover_base_properties(rover_at_middle, square_plataeu):
    assert rover_at_middle.plateau == square_plataeu
    assert rover_at_middle.name == "Rover Middle"
    assert rover_at_middle.current_x == 3
    assert rover_at_middle.current_y == 3
    assert rover_at_middle.current_orientation == Orientation.N


def test_turn_left(rover_at_middle):
    rover_at_middle.turn_left()
    assert rover_at_middle.current_orientation == Orientation.W

    rover_at_middle.turn_left()
    rover_at_middle.turn_left()
    assert rover_at_middle.current_orientation == Orientation.E


def test_turn_right(rover_at_edge):
    rover_at_edge.turn_right()
    assert rover_at_edge.current_orientation == Orientation.W

    rover_at_edge.turn_right()
    rover_at_edge.turn_right()
    rover_at_edge.turn_right()
    assert rover_at_edge.current_orientation == Orientation.S


def test_move_forward(rover_at_middle):
    rover_at_middle.move_forward()  # 3 3
    assert rover_at_middle.current_x == 3
    assert rover_at_middle.current_y == 4

    rover_at_middle.turn_right()
    rover_at_middle.move_forward()  # 3 4
    assert rover_at_middle.current_x == 4
    assert rover_at_middle.current_y == 4

    rover_at_middle.turn_left()
    rover_at_middle.turn_left()
    rover_at_middle.move_forward()  # 4 4
    rover_at_middle.move_forward()
    assert rover_at_middle.current_x == 2
    assert rover_at_middle.current_y == 4


def test_move_out_of_borders(rover_at_dot):
    expected_msg = "Crossing {} border"
    with pytest.raises(InvalidRoverOperationException) as ex:
        rover_at_dot.move_forward()
    assert ex.value.message == expected_msg.format("upper")

    with pytest.raises(InvalidRoverOperationException) as ex:
        rover_at_dot.turn_right()
        rover_at_dot.move_forward()
    assert ex.value.message == expected_msg.format("right")

    with pytest.raises(InvalidRoverOperationException) as ex:
        rover_at_dot.turn_right()
        rover_at_dot.move_forward()
    assert ex.value.message == expected_msg.format("lower")

    with pytest.raises(InvalidRoverOperationException) as ex:
        rover_at_dot.turn_right()
        rover_at_dot.move_forward()
    assert ex.value.message == expected_msg.format("left")


def test_report_status(rover_at_middle, rover_at_edge):
    output_template = "{}:{} {} {}"
    assert rover_at_middle.report_status() == (
        output_template.format(rover_at_middle.name,
                               rover_at_middle.current_x,
                               rover_at_middle.current_y,
                               rover_at_middle.current_orientation.name))

    output_template = "{}:{} {} {}"
    assert rover_at_edge.report_status() == (
        output_template.format(rover_at_edge.name,
                               rover_at_edge.current_x,
                               rover_at_edge.current_y,
                               rover_at_edge.current_orientation.name))


def test_parse_rover_input_base(square_plataeu):
    good_input_landing = "Rover1 Landing:1 2 N"
    Rover.parse_rover_input(good_input_landing, square_plataeu)
    assert Rover.get_rover_by_name("Rover1")

    good_input_instructions = "Rover1 Instructions:LMLMLMLMM"
    Rover.parse_rover_input(good_input_instructions, square_plataeu)
    assert Rover.get_rover_by_name("Rover1").current_y == 3


def test_parse_rover_input_invalid(square_plataeu):
    expected_msg = "Invalid Rover input"
    no_colon = "Rover1 Landing 1 2 N"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_rover_input(no_colon, square_plataeu)
    assert ex.value.message == expected_msg

    too_many_colons = "Rover1:Landing:1 2 N"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_rover_input(too_many_colons, square_plataeu)
    assert ex.value.message == expected_msg

    expected_msg = "Unknown rover input type: {}"
    unknown_command = "Rover1 Restart:1 2 N"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_rover_input(unknown_command, square_plataeu)
    assert ex.value.message == expected_msg.format("Restart")


def test_parse_landing_base(square_plataeu):
    rover_name = "Rover5"
    landing_input = "1 2 W"
    Rover.parse_landing(rover_name, landing_input, square_plataeu)

    new_rover = Rover.get_rover_by_name(rover_name)
    assert new_rover
    assert new_rover.name == rover_name
    assert new_rover.current_x == 1
    assert new_rover.current_y == 2
    assert new_rover.current_orientation == Orientation.W
    assert new_rover.plateau == square_plataeu


def test_parse_landing_invalid_input(square_plataeu):
    expected_msg = "Invalid rover landing input"

    no_space_input = "12N"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_landing("name", no_space_input, square_plataeu)
    assert ex.value.message == expected_msg

    too_many_spaces = "1 2   N 4"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_landing("name", too_many_spaces, square_plataeu)
    assert ex.value.message == expected_msg

    empty_input = ""
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_landing("name", empty_input, square_plataeu)
    assert ex.value.message == expected_msg


def test_parse_landing_invalid_coor(square_plataeu):
    expected_msg = "Invalid rover landing coordinates input: {}"

    non_numerics = "A 2 N"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_landing("name", non_numerics, square_plataeu)
    assert ex.value.message == expected_msg.format(non_numerics)

    floats_coors = "3 2.9 N"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_landing("name", floats_coors, square_plataeu)
    assert ex.value.message == expected_msg.format(floats_coors)


def test_parse_landing_unknown_orientation(square_plataeu):
    expected_msg = "Invalid rover orientation input: {}"

    wrong_orientation = "2 2 A"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_landing("name", wrong_orientation, square_plataeu)
    assert ex.value.message == expected_msg.format('A')


def test_parse_landing_out_of_border(square_plataeu):
    out_of_border = "100 1 E"
    with pytest.raises(InvalidRoverOperationException) as ex:
        Rover.parse_landing("name", out_of_border, square_plataeu)
    assert ex.value.message == "Crossing right border"

    negative_landing = "-1 1 N"
    with pytest.raises(InvalidRoverOperationException) as ex:
        Rover.parse_landing("name", negative_landing, square_plataeu)
    assert ex.value.message == "Crossing left border"


def test_parse_instructions_base(rover_at_middle, rover_registry):
    Rover.rover_registry = rover_registry

    good_input = "LMLMLMLMRMRMRMRMMLM"
    Rover.parse_instructions(rover_at_middle.name, good_input)

    turn_only = "LLLLRRRRLRLRLRRRLRLRLR"
    Rover.parse_instructions(rover_at_middle.name, turn_only)

    empty_input = ""
    Rover.parse_instructions(rover_at_middle.name, empty_input)


def test_parse_instructions_unkonwn_rover(rover_registry):
    expected_msg = "Rover {} does not exist"
    Rover.rover_registry = rover_registry

    non_existing_name = "Rover874"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_instructions(non_existing_name, "")
    assert ex.value.message == expected_msg.format(non_existing_name)

    empty_name = ""
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_instructions(non_existing_name, "")
    assert ex.value.message == expected_msg.format(non_existing_name)


def test_parse_instructions_unknown_command(rover_registry, rover_at_middle):
    expected_msg = "Unknown rover instruction: {}"
    Rover.rover_registry = rover_registry

    unknown_command = "LMRCLLRRLR"
    with pytest.raises(InvalidInputException) as ex:
        Rover.parse_instructions(rover_at_middle.name, unknown_command)
    assert ex.value.message == expected_msg.format('C')


def test_report_all(rover_registry):
    Rover.rover_registry = rover_registry
    Rover.report_all_rovers()
