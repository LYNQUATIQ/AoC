import logging
import os

from collections import defaultdict, deque
from itertools import combinations

from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_25.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=file_path,
    filemode="w",
)

file_path = os.path.join(script_dir, "inputs/day_25_input.txt")
with open(file_path) as f:
    program_str = f.read()
program = [int(x) for x in program_str.split(",")]

computer = IntCodeComputer(program)

command_dict = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
}

steps = [
    "east",
    "east",
    "east",
    "take shell",
    "west",
    "south",
    "take monolith",
    "north",
    "west",
    "north",
    "west",
    "take bowl of rice",
    "east",
    "north",
    "west",
    "take ornament",
    "south",
    "south",
    "take fuel cell",
    "north",
    "north",
    "east",
    "take planetoid",
    "east",
    "take cake",
    "south",
    "west",
    "north",
    "take astrolabe",
    "west",
    "inv",
]

inventory = [
    "monolith",
    "bowl of rice",
    "ornament",
    "shell",
    "astrolabe",
    "planetoid",
    "fuel cell",
    "cake",
]


def enter_input(input_string):
    input_string = command_dict.get(input_string, input_string)
    input_values = [ord(c) for c in input_string] + [10]
    computer.run_program(input_values)
    return computer.ascii_output(clear_output=True)


# Get to the security checkpoint
for step in steps:
    enter_input(step)

# Drop all the stuff in your inventory
for item in inventory:
    enter_input(f"drop {item}")


class GotThroughCheckpoint(Exception):
    pass


# Try all combinations
try:
    for n in range(4, len(inventory) + 1):
        for items in combinations(inventory, n):

            print(f"Testing: {items}")
            # Pick up the items
            for item in items:
                enter_input(f"take {item}")

            # Try and go through checkpoint
            response = enter_input("north")
            if "ejected back" not in response:
                print(response)
                raise GotThroughCheckpoint

            # Drop the items
            for item in items:
                enter_input(f"drop {item}")

except GotThroughCheckpoint:
    pass
