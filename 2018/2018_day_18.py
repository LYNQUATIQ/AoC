import logging
import os
import re

from collections import defaultdict

from grid_system import ConnectedGrid, XY

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_18.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, f"inputs/2018_day_18_input.txt")
lines = [line.rstrip("\n") for line in open(file_path)]


class Wood(ConnectedGrid):
    LUMBERYARD = "#"
    OPEN = "."
    TREE = "|"

    # symbols = {
    #     LUMBERYARD: "\U00002692",
    #     TREE: "\U0001F332",
    #     OPEN: " ",
    # }

    BLANK = OPEN

    def __init__(self, lines):
        super().__init__()
        self.load_grid(lines)

    def number_surrounding(self, xy):
        number_surrounding = defaultdict(int)
        for nb in xy.neighbours_including_diagonals:
            number_surrounding[self.get_symbol(nb)] += 1
        return number_surrounding

    def process_round(self):
        new_grid = {}
        x_range, y_range = self.get_ranges()
        for y in y_range:
            for x in x_range:
                xy = XY(x, y)
                symbol = self.get_symbol(xy)
                new_symbol = symbol
                number_surrounding = self.number_surrounding(xy)
                if symbol == self.OPEN:
                    if number_surrounding[self.TREE] >= 3:
                        new_symbol = self.TREE
                elif symbol == self.TREE:
                    if number_surrounding[self.LUMBERYARD] >= 3:
                        new_symbol = self.LUMBERYARD
                elif symbol == self.LUMBERYARD:
                    if not (
                        number_surrounding[self.LUMBERYARD] >= 1
                        and number_surrounding[self.TREE] >= 1
                    ):
                        new_symbol = self.OPEN
                new_grid[xy] = new_symbol
        self.grid = new_grid

    def resource_value(self):
        resource_values = defaultdict(int)
        for symbol in self.grid.values():
            resource_values[symbol] += 1
        return resource_values[self.LUMBERYARD] * resource_values[self.TREE]


wood = Wood(lines)
minutes = 0
for minutes in range(1000000000):
    print(f"Minute: {minutes}  Resource value: {wood.resource_value()}")
    wood.process_round()
