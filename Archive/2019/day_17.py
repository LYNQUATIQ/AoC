import os

from intcode_computer import IntCodeComputer
from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
program = [int(i) for i in lines[0].split(",")]


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
        steps, at_end = 0, False
        while not at_end:
            next_loc = self.robot_loc + self.robot_step
            if self.grid.get(next_loc, self.SPACE) != self.SPACE:
                steps += 1
                self.robot_loc = next_loc
                continue

            if steps != 0:
                instructions.append(str(steps))

            turn_made = self.try_turning()
            if turn_made:
                instructions.append(turn_made)
                steps = 0
                continue

            break

        return instructions

    def load_element(self, xy, c):
        if c in self.robot_facing.keys():
            self.robot_loc = xy
            self.robot_step = self.robot_facing[c]
            self.robot_symbol = c
            c = self.SCAFFOLD
        self.grid[xy] = c

    def run_image_scanner(self, program):
        self.computer = IntCodeComputer(program)
        self.computer.run_program()
        x, y = 0, 0
        for c in self.computer.output():
            if c == 10:
                y += 1
                x = 0
            else:
                self.load_element(XY(x, y), chr(c))
                x += 1

    def find_intersections(self):
        intersections = []
        for loc, c in self.grid.items():
            if c == self.SCAFFOLD:
                cross_section = [self.grid.get(nb, None) for nb in loc.neighbours]
                if all([i == self.SCAFFOLD for i in cross_section]):
                    intersections.append(loc)
        return intersections


system = AsciiSystem()
system.run_image_scanner(program)
intersections = system.find_intersections()
print(f"Part 1: {sum(i.x * i.y for i in intersections)}")


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

    start = 0
    while string[start] not in boundaries:
        start += 1
        if start > len(string):
            return None
    extent = start

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
            token_dict[token] = substring
            return token_dict

    return None


path = system.traverse_path()
path = ",".join(path) + ","
token_dict = tokenise_string(path)
tokens = sorted(token_dict.keys())
for token in tokens:
    path = path.replace(token_dict[token], token)
    routine = token_dict[token][:-1]
    token_dict[token] = [ord(c) for c in routine] + [10]
main_routine = [ord(c) for c in ",".join(c for c in path)] + [10]

computer = IntCodeComputer(program, {0: 2})
computer.run_program()
computer.run_program(main_routine)
for token in tokens:
    computer.run_program(token_dict[token])
computer.run_program([ord("n"), 10])
print(f"Part 2: {computer.last_output()}")
