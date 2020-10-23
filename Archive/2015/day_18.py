import logging
import os

from itertools import product

from grid_system import ConnectedGrid, XY


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

class LightGrid(ConnectedGrid):

    ON = "#"
    OFF = "."

    def __init__(self, lines, always_on=[]):
        super().__init__()
        self.always_on = always_on
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                self.grid[XY(x, y)] = c
        self.max_x = x + 1
        self.max_y = y + 1

    def lit_neighbours(self, xy):
        directions = [XY(-1, -1), XY(-1, 0), XY(-1, +1), XY(+1, -1), XY(+1, 0), XY(+1, +1), XY(0, -1), XY(0, +1)]
        return sum(self.grid.get(xy + d, self.OFF) == self.ON for d in directions)
    
    def update_grid(self, n_times=1):
        for _ in range(n_times):
            new_grid = {}
            for x, y in product(range(self.max_x), range(self.max_y)):
                xy = XY(x, y)
                xy_lit = self.grid[xy] == self.ON
                n_lit = self.lit_neighbours(xy)
                if xy in self.always_on or (xy_lit and n_lit in [2, 3]) or (not xy_lit and n_lit == 3):
                    new_grid[xy] = self.ON
                else:
                    new_grid[xy] = self.OFF
            self.grid = new_grid

    def number_lit(self):
        return sum(i == self.ON for i in self.grid.values())


grid = LightGrid(lines)
grid.update_grid(100)
print(f"Part 1: {grid.number_lit()}")

grid = LightGrid(lines, always_on=[XY(0, 0), XY(0, 99), XY(99, 0), XY(99, 99)])
grid.update_grid(100)
print(f"Part 1: {grid.number_lit()}")