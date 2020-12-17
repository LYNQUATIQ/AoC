import os

from utils import print_time_taken
from grid import Point

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """.#.
..#
###"""


class ConwayCubes:
    def __init__(self, inputs, dimensions):
        self.active = set()
        for y, line in enumerate(inputs.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    pt = (x, y) + (0,) * (dimensions - 2)
                    self.active.add(Point(*pt))

    def boot_up(self):
        for _ in range(6):
            to_consider = set(self.active)
            for pt in self.active:
                to_consider.update(pt.neighbours)
            new_active = set()
            for pt in to_consider:
                n_count = sum(n in self.active for n in pt.neighbours)
                if n_count not in [2, 3]:
                    continue
                if pt in self.active or n_count == 3:
                    new_active.add(pt)
            self.active = new_active
        return len(self.active)


@print_time_taken
def solve(inputs):
    print(f"Part 1: {ConwayCubes(inputs, dimensions=3).boot_up()}")
    print(f"Part 2: {ConwayCubes(inputs, dimensions=4).boot_up()}\n")


solve(sample_input)
solve(actual_input)
