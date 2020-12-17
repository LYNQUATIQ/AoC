import os

from itertools import product
from utils import print_time_taken

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """
.#.
..#
###
"""


class NDimensionsalPoint(tuple):
    @property
    def neighbours(self):
        return [
            self + type(self)(direction)
            for direction in product(*([[-1, 0, 1]] * len(self)))
            if not all(d == 0 for d in direction)
        ]

    def __add__(self, other):
        return type(self)(a + b for a, b in zip(self, other))


class ConwayCubes:
    def __init__(self, inputs, dimensions):
        self.active = set()
        for y, line in enumerate(inputs.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    pt = NDimensionsalPoint([x, y] + [0] * (dimensions - 2))
                    self.active.add(pt)

    def iterate(self):
        new_active = set()

        to_consider = set(self.active)
        for pt in self.active:
            to_consider.update(pt.neighbours)

        for pt in to_consider:
            n_count = sum(n in self.active for n in pt.neighbours)
            if pt in self.active:
                if n_count in [2, 3]:
                    new_active.add(pt)
            else:
                if n_count == 3:
                    new_active.add(pt)
        self.active = new_active

    def iterate_cycles(self):
        for _ in range(6):
            self.iterate()
        return len(self.active)


@print_time_taken
def solve(inputs):
    cubes = ConwayCubes(inputs, dimensions=3)
    print(f"Part 1: {cubes.iterate_cycles()}")
    cubes = ConwayCubes(inputs, dimensions=4)
    print(f"Part 2: {cubes.iterate_cycles()}\n")


solve(sample_input)
solve(actual_input)
