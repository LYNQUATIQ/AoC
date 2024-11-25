import logging
import os
import string

from grid_system import ConnectedGrid, XY


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_19.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_19_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Network(ConnectedGrid):
    CORNER = "+"
    HORIZONTAL = "-"
    VERTICAL = "|"

    UP = XY(0, -1)
    DOWN = XY(0, 1)
    RIGHT = XY(1, 0)
    LEFT = XY(-1, 0)

    turns = {
        UP: ((LEFT, RIGHT), HORIZONTAL),
        DOWN: ((LEFT, RIGHT), HORIZONTAL),
        RIGHT: ((UP, DOWN), VERTICAL),
        LEFT: ((UP, DOWN), VERTICAL),
    }

    def __init__(self, lines):
        super().__init__()
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if c != " ":
                    self.grid[XY(x, y)] = c
                    if y == 0:
                        self.start = XY(x, y)
                x += 1
            y += 1
        self.max_x = x
        self.max_y = y

    def navigate(self):
        letters_passed = ""
        steps = 0
        xy = self.start
        direction = self.DOWN
        while True:
            xy += direction
            steps += 1
            symbol = self.grid.get(xy, None)
            if symbol is None:
                break

            if symbol in string.ascii_letters:
                letters_passed += symbol
                continue

            if symbol == self.CORNER:
                directions, s = self.turns[direction]
                direction = None
                for d in directions:
                    if self.grid.get(xy + d, None) == s:
                        direction = d
                assert direction

        return letters_passed, steps


network = Network(lines)
letters_passed, steps = network.navigate()
print(f"Part 1: {letters_passed}")
print(f"Part 2: {steps}")
