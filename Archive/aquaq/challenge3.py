import logging
import os

import re

from collections import defaultdict

from grid_system import ConnectedGrid, XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
directions = lines[0]


class Diamond(ConnectedGrid):
    ROOM = "#"
    WALL = " "

    def __init__(self):
        super().__init__()

        lines = [
            "  ##  ",
            " #### ",
            "######",
            "######",
            " #### ",
            "  ##  ",
        ]
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                xy = XY(x, y)
                self.grid[xy] = c
                x += 1
            y += 1
        self.position = XY(2, 0)

    def connected_nodes(self, node, blockages=None):
        return [n for n in node.neighbours if self.grid[n] != self.WALL]

    def make_move(self, direction):
        move = {
            "R": self.EAST,
            "U": self.NORTH,
            "D": self.SOUTH,
            "L": self.WEST,
        }[direction]
        new_pos = self.position + move
        if self.grid.get(new_pos, self.WALL) != self.WALL:
            self.position = new_pos


grid = Diamond()
output = 0
for direction in directions:
    grid.make_move(direction)
    output += grid.position.manhattan_distance
    print(f"Moved {direction} -> {grid.position}")

print(f"ANSWER = {output}")
