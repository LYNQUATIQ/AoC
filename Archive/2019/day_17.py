import logging
import os
from abc import ABC, abstractmethod
from collections import deque
from typing import NamedTuple

from intcode_computer import IntCodeComputer
from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_17.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)
file_path = os.path.join(script_dir, "inputs/day_17_input.txt")
with open(file_path) as f:
    program = f.read()
program = [int(x) for x in program.split(",")]

file_path = os.path.join(script_dir, "inputs/day_17_map_input.txt")
map_image = [line.rstrip("\n") for line in open(file_path)]


class AsciiSystem(ConnectedGrid):

    SPACE = "."
    SCAFFOLD = "#"
    ROBOT_N = "^"
    ROBOT_E = ">"
    ROBOT_S = "v"
    ROBOT_W = "<"

    robot_facing = {
        ROBOT_N: ConnectedGrid.NORTH,
        ROBOT_E: ConnectedGrid.EAST,
        ROBOT_S: ConnectedGrid.SOUTH,
        ROBOT_W: ConnectedGrid.WEST,
    }

    def __init__(self):
        super().__init__()
        self.max_x, self.max_y = 0, 0

    def try_turning(self):
        possible_turns = [
            ("L", self.turn_left(self.robot_step)),
            ("R", self.turn_right(self.robot_step)),
        ]
        for instruction, turn in possible_turns:
            next_loc = self.robot_loc + turn
            if self.grid.get(next_loc, self.SPACE) == self.SPACE:
                continue
            self.robot_step = turn
            return instruction
        return None

    def traverse_path(self):
        instructions = []
        steps = 0
        at_end = False
        while not at_end:
            next_loc = self.robot_loc + self.robot_step
            if self.grid.get(next_loc, self.SPACE) != self.SPACE:
                steps += 1
                self.robot_loc = next_loc
                continue

            # Store steps instruction and make turn
            if steps != 0:
                instructions.append(str(steps))

            turn_made = self.try_turning()
            if turn_made:
                instructions.append(turn_made)
                steps = 0
                continue

            # No possible turn - must have got to end!
            break

        return instructions

    def load_element(self, xy, c):
        if c in self.robot_facing.keys():
            self.robot_loc = xy
            self.robot_step = self.robot_facing[c]
            self.robot_symbol = c
            c = self.SCAFFOLD
        self.grid[xy] = c

    def load_image(self, map_image):
        for y, scan_line in enumerate(map_image):
            for x, c in enumerate(scan_line):
                self.load_element(XY(x, y), c)
        self.max_x = x + 1
        self.max_y = y + 1
        # self.print_image()

    def run_image_scanner(self, program):
        self.computer = IntCodeComputer(program)
        self.computer.run_program()
        self.scan_image(self.computer.output())
        # self.print_image()

    def scan_image(self, image):
        x, y = 0, 0
        for c in image:
            self.max_y = max(self.max_y, y)
            if c == 10:
                y += 1
                x = 0
            else:
                self.load_element(XY(x, y), chr(c))
                x += 1
            self.max_x = max(self.max_x, x)

    def print_image(self):
        header1 = "              1         2         3         4  "
        header2 = "    0123456789012345678901234567890123456789012"
        print(header1)
        print(header2)
        for y in range(self.max_y):
            print(f"{y:3d} ", end="")
            for x in range(self.max_x):
                loc = XY(x, y)
                c = self.grid.get(loc, self.SPACE)
                if loc == self.robot_loc:
                    c = self.robot_symbol
                print(c, end="")
            print(f" {y:<3d} ")
        print(header2)
        print(header1)

    def connected_nodes(self, node):
        return [n for n in node.neighbours if self.grid.get(n, None) == self.SCAFFOLD]

    def find_intersections(self):
        intersections = []
        for loc, c in self.grid.items():
            if c == self.SCAFFOLD:
                cross_section = [self.grid.get(nb, None) for nb in loc.neighbours]
                if all([i == self.SCAFFOLD for i in cross_section]):
                    intersections.append(loc)
        return intersections


def tokenise_string(
    string, tokens_left="ABC", tokens_used="", max_token_length=21, boundaries="RL"
):

    if all(c in tokens_used for c in string):
        return {}

    if not tokens_left:
        return None

    token = tokens_left[0]
    tokens_left = tokens_left[1:]
    tokens_used += token

    # Find first character that needs tokenising
    start = 0
    while string[start] not in boundaries:
        start += 1
        if start > len(string):
            return None
    extent = start
    max_extent = min(max_token_length + start, len(string))

    while True:
        extent += 1
        while string[extent] not in boundaries:
            extent += 1
            if extent == len(string):
                break
            if extent >= start + max_token_length:
                return None
            if string[extent] in tokens_used:
                break
        substring = string[start:extent]
        tokenised_string = string.replace(substring, token)

        token_dict = tokenise_string(
            tokenised_string, tokens_left, tokens_used, max_token_length, boundaries
        )
        if token_dict is not None:
            # Success
            token_dict[token] = substring
            return token_dict

    return None


system = AsciiSystem()
system.run_image_scanner(program)
system.load_image(map_image)

# intersections = system.find_intersections()
# print(sum(i.x * i.y for i in intersections))

path = system.traverse_path()
path = ",".join(path) + ","
token_dict = tokenise_string(path)
tokens = sorted(token_dict.keys())
for token in tokens:
    path = path.replace(token_dict[token], token)
    routine = token_dict[token][:-1]
    token_dict[token] = [ord(c) for c in routine] + [10]
    print(f"{token} - {token_dict[token]}")
main_routine = [ord(c) for c in ",".join(c for c in path)] + [10]
print(main_routine)

computer = IntCodeComputer(program, 2)


def run_computer(input_values=[]):
    computer.run_program(input_values)
    print(input_values)
    print("".join([chr(c) for c in computer.output()]))


run_computer()
run_computer(main_routine)
for token in tokens:
    run_computer(token_dict[token])
computer.run_program([ord("n"), 10])
print(computer.output())

