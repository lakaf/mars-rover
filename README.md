# Mars Rover Parser

## About

Mars Rover parse is a command line program that parses text inputs containing plateau info, rovers' landing info as well as instructions, and in the end prints out the report of the status of all rovers.

---

1. [Quick Start](#quick-start)
1. [System Requirements](#system-requirements)
1. [Usage](#usage)
1. [Input Format](#input-format)
1. [Output Example](#output-example)

---

## Quick Start

```
# Pass input through file
python3 -m marsrover sample_input.txt

# Pass input through inline command line
python3 -m marsrover "Plateau:5 5
Rover1 Landing:1 2 N
Rover1 Instructions:LMLMLMLMM
Rover2 Landing:3 3 E
Rover2 Instructions:MMRMMRMRRM"
```

---

## System Requirements

- Python 3.7.6 or later
- pytest module 6.1.1 or later (only if you want to run unit testing locally)

---

## Usage

```
python3 -m marsrover <input_file_path>
# OR
python3 -m marsrover <inline_text_input>
```

Running under debug mode, which will show more detailed exception message:

```
python3 -m marsrover --debug <input_file_path>
# OR
python3 -m marsrover --debug <inline_text_input>
```

See command line help:

```
python3 -m marsrover --help
```

---

## Input Format

Input file has to be provided in proper format:

- First line of it must be the configuration of the Plateau where the rovers will be landed on.<br/>
  It will include name of plateau, and upper-right coordinates of the plateau, separated by a colon:<br/>

  ```
  Plateau:5 5
  ```

- Following lines of the input file will describe either landing or instructions for rovers.<br/>
  - Landing input will consist of rover's name, **Landing** keyword, initial x and y coordinates where the rover lands on, and the rover's initial orientation (could be 'N', 'W', 'S' or 'E), formatted as following:
    ```
    Rover1 Landing:1 2 N
    ```
  - Instructions input will consist of rover's name (needs to be matching with the name in Landing input), **Instructions** keyword, and a list of characters representing 3 types of instructions ('L' for left turn, 'R' for right turn, and 'M' for move forward), formatted as following:
    ```
    Rover1 Instructions:LMLMLMLMMRMLR
    ```

You can get a simple sample input from the included `sample_input.txt` file.

## Output Example

```
python3 -m marsrover sample_input.txt sample_input.txt
Rover1:1 3 N
Rover2:5 1 E
```

## Unit testing

A shell script wrapper has been provided to run the unit tests as well (please make sure your default python3 runtime has pytest 6.1.1 or later installed):

```
./unit-test
```
