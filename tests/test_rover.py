import pytest
from marsrover.enums import Orientation
from marsrover.exceptions import (InvalidInputException,
                                  InvalidRoverOperationException)
from marsrover.models import Plateau, Rover
from marsrover.parsers import RoverLandingTextParser, RoverMovingTextParser
from marsrover.database import RoverMemoryRepo


@pytest.fixture()
def rover_repo():
    return RoverMemoryRepo()


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
def rover_at_next_to_middle(square_plataeu):
    return Rover(
        square_plataeu,
        "Rover Next to Middle",
        3, 2, Orientation.N
    )


@pytest.fixture()
def rover_landing_parser(square_plataeu, rover_repo):
    return RoverLandingTextParser(square_plataeu, rover_repo)


@pytest.fixture()
def rover_moving_parser(square_plataeu, rover_repo):
    return RoverMovingTextParser(square_plataeu, rover_repo)


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


def test_parse_rover_input_base(
        rover_landing_parser, rover_moving_parser, rover_repo):
    good_input_landing = "RoverBase Landing:1 2 N"
    rover_landing_parser.parse_input_line(good_input_landing)
    assert rover_repo.get_rover_by_name("RoverBase")

    good_input_instructions = "RoverBase Instructions:LMLMLMLMM"
    rover_moving_parser.parse_input_line(good_input_instructions)
    assert rover_repo.get_rover_by_name("RoverBase").current_y == 3


def test_parse_rover_input_invalid(rover_landing_parser):
    expected_msg = "Invalid Rover input"
    no_colon = "Rover1 Landing 1 2 N"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(no_colon)
    assert ex.value.message == expected_msg

    too_many_colons = "Rover1:Landing:1 2 N"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(too_many_colons)
    assert ex.value.message == expected_msg


def test_parse_landing_base(rover_landing_parser, rover_repo, square_plataeu):
    rover_name = "RoverLandingBase"
    landing_input = "RoverLandingBase Landing:1 2 W"
    rover_landing_parser.parse_input_line(landing_input)

    new_rover = rover_repo.get_rover_by_name(rover_name)
    assert new_rover
    assert new_rover.name == rover_name
    assert new_rover.current_x == 1
    assert new_rover.current_y == 2
    assert new_rover.current_orientation == Orientation.W
    assert new_rover.plateau == square_plataeu


def test_parse_landing_twice(rover_landing_parser):
    rover_name = "RoverTwice"
    landing_input = "RoverTwice Landing:1 2 W"
    expected_msg = "Rover {} has already landed before"
    rover_landing_parser.parse_input_line(landing_input)

    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(landing_input)
    assert ex.value.message == expected_msg.format(rover_name)


def test_parse_landing_invalid_input(rover_landing_parser):
    expected_msg = "Invalid rover landing input"

    no_space_input = "Rover1 Landing:12N"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(no_space_input)
    assert ex.value.message == expected_msg

    too_many_spaces = "Rover1 Landing:1 2   N 4"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(too_many_spaces)
    assert ex.value.message == expected_msg


def test_parse_landing_invalid_coor(rover_landing_parser):
    expected_msg = "Invalid rover landing coordinates input: {}"

    non_numerics = "Rover1 Landing:A 2 N"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(non_numerics)
    assert ex.value.message == expected_msg.format("A 2 N")

    floats_coors = "Rover1 Landing:3 2.9 N"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(floats_coors)
    assert ex.value.message == expected_msg.format("3 2.9 N")


def test_parse_landing_unknown_orientation(rover_landing_parser):
    expected_msg = "Invalid rover orientation input: {}"

    wrong_orientation = "Rover1 Landing:2 2 A"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(wrong_orientation)
    assert ex.value.message == expected_msg.format('A')


def test_parse_landing_out_of_border(rover_landing_parser):
    out_of_border = "Rover1 Landing:100 1 E"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(out_of_border)
    assert ex.value.message == "Invalid landing location: (100, 1)"

    negative_landing = "Rover1 Landing:-1 1 N"
    with pytest.raises(InvalidInputException) as ex:
        rover_landing_parser.parse_input_line(negative_landing)
    assert ex.value.message == "Invalid landing location: (-1, 1)"


def test_parse_instructions_base(rover_moving_parser, rover_landing_parser):
    rover_landing_parser.parse_input_line("RoverBase Landing: 3 3 N")

    good_input = "RoverBase Instructions:LMLMLMLMRMRMRMRMMLM"
    rover_moving_parser.parse_input_line(good_input)

    turn_only = "RoverBase Instructions:LLLLRRRRLRLRLRRRLRLRLR"
    rover_moving_parser.parse_input_line(turn_only)

    empty_input = "RoverBase Instructions:"
    rover_moving_parser.parse_input_line(empty_input)


def test_parse_instructions_unkonwn_rover(rover_moving_parser):
    expected_msg = "Rover {} does not exist"

    non_existing_name = "Rover874 Instructions:L"
    with pytest.raises(InvalidInputException) as ex:
        rover_moving_parser.parse_input_line(non_existing_name)
    assert ex.value.message == expected_msg.format("Rover874")


def test_parse_instructions_unknown_command(rover_moving_parser, rover_landing_parser):
    rover_landing_parser.parse_input_line("RoverBase Landing: 3 3 N")
    expected_msg = "Unknown rover instruction: {}"
    Rover.rover_registry = rover_registry

    unknown_command = "RoverBase Instructions:LMRCLLRRLR"
    with pytest.raises(InvalidInputException) as ex:
        rover_moving_parser.parse_input_line(unknown_command)
    assert ex.value.message == expected_msg.format('C')


def test_report_all(rover_repo, rover_landing_parser):
    rover_repo.report_all_rovers()
    rover_landing_parser.parse_input_line("RoverBase Landing: 3 3 N")
    rover_repo.report_all_rovers()


def test_rover_collision(rover_at_middle, rover_at_next_to_middle):
    rover_at_middle.plateau.update_occupied_location(rover_at_middle)
    with pytest.raises(InvalidRoverOperationException) as ex:
        rover_at_next_to_middle.move_forward()
