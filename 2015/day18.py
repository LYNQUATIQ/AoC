import os

from grid_system import XY

with open(os.path.join(os.path.dirname(__file__), "inputs/day18_input.txt")) as f:
    actual_input = f.read()

sample_input = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""


class LightGrid:
    def __init__(self, inputs, corners_on=False):
        self.lit = set()
        x, y = 0, 0
        for y, line in enumerate(inputs.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    self.lit.add(XY(x, y))
        self.always_on = set()
        if corners_on:
            self.always_on = set([XY(0, 0), XY(x, 0), XY(0, y), XY(x, y)])
            for xy in self.always_on:
                self.lit.add(xy)
        self.max_x, self.max_y = x, y

    def iterate(self, n_times):
        for _ in range(n_times):
            to_consider = set(self.lit)
            for xy in self.lit:
                to_consider.update(n for n in xy.all_neighbours)
            new_lit = set()
            for xy in to_consider:
                if not xy.in_bounds(self.max_x, self.max_y):
                    continue
                currently_lit = xy in self.lit
                n_count = sum(n in self.lit for n in xy.all_neighbours)
                if (
                    xy in self.always_on
                    or (currently_lit and n_count in [2, 3])
                    or (not currently_lit and n_count == 3)
                ):
                    new_lit.add(xy)
            self.lit = new_lit
        return len(self.lit)


def solve(inputs, iterations=100):
    print(f"Part 1: {LightGrid(inputs).iterate(iterations)}")
    print(f"Part 2: {LightGrid(inputs, corners_on=True).iterate(iterations)}\n")


solve(sample_input, 5)
solve(actual_input)
