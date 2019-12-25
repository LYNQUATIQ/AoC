import logging
import os

from grid_system import XY, ConnectedGrid
from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_21.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, "inputs/day_21_input.txt")
with open(file_path) as f:
    program_str = f.read()
program = [int(x) for x in program_str.split(",")]


computer = IntCodeComputer(program)
script = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT D T",
    "OR H T",
    "OR E T",
    "AND T J",
    "RUN",
]

for line in script:
    computer.run_program([ord(c) for c in line] + [10])
    print(computer.ascii_output())
    # print("".join(chr(c) for c in computer.output()[:-1]))
    # if computer.last_output() != 10:
    #     print(computer.last_output())

