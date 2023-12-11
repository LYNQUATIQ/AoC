"""https://adventofcode.com/2018/day/17"""
import os
import re
import sys

from itertools import product
from typing import NamedTuple

from utils import print_time_taken


with open(os.path.join(os.path.dirname(__file__), "inputs/day17_input.txt")) as f:
    actual_input = f.read()

sample_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

REGEX = re.compile(
    r"^(?P<xy1>x|y)=(?P<level>-?\d+), (?P<xy2>x|y)=(?P<low>-?\d+)..(?P<high>-?\d+)$"
)


class XY(NamedTuple("Pt", [("x", int), ("y", int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)


class Reservoir:  # (ConnectedGrid):
    CLAY = "#"
    SAND = "."
    SPRING = "+"
    FLOWING = "|"
    STANDING = "~"

    WATER = [STANDING, FLOWING]
    PERMEABLE = [SAND, FLOWING]
    IMPERMEABLE = [CLAY, STANDING]

    def get_symbol(self, xy):
        blank = self.SAND
        if xy.y < 0:
            blank = " "
        return self.grid.get(xy, blank)

    def __init__(self, inputs):
        self.spring_xy = XY(500, 0)
        self.top, self.bottom = sys.maxsize, 0
        self.grid = {self.spring_xy: self.SPRING}
        for line in inputs.splitlines():
            regex = REGEX.match(line).groupdict()
            clay_scan = {
                regex["xy1"]: (int(regex["level"]), int(regex["level"]) + 1),
                regex["xy2"]: (int(regex["low"]), int(regex["high"]) + 1),
            }
            self.top = min(clay_scan["y"][0], self.top)
            self.bottom = max(clay_scan["y"][1] - 1, self.bottom)
            for x, y in product(range(*clay_scan["x"]), range(*clay_scan["y"])):
                self.grid[XY(x, y)] = self.CLAY
        self.flood_fill()

    def material(self, xy):
        return self.grid.get(xy, self.SAND)

    def flood_fill(self):
        to_flood_from = [self.spring_xy]
        flooded_from = set()
        while to_flood_from:
            xy = to_flood_from.pop()
            flooded_from.add(xy)

            # Flow down until we hit clay (or standing WATER) or go past bottom
            while self.material(xy + XY(0, 1)) == self.SAND and xy.y < self.bottom:
                xy += XY(0, 1)
                if xy.y >= self.top:
                    self.grid[xy] = self.FLOWING

            if xy.y == self.bottom:
                continue

            # Get left and right limits
            xy_left, xy_right = xy, xy
            while (
                self.material(xy_left + XY(0, 1)) in self.IMPERMEABLE
                and self.material(xy_left + XY(-1, 0)) != self.CLAY
            ):
                xy_left += XY(-1, 0)
                self.grid[xy_left] = self.FLOWING
            while (
                self.material(xy_right + XY(0, 1)) in self.IMPERMEABLE
                and self.material(xy_right + XY(1, 0)) != self.CLAY
            ):
                xy_right += XY(1, 0)
                self.grid[xy_right] = self.FLOWING

            # If not contained by clay then flood from left and right limits,
            # Otherwise convert to standing WATER and flood from one above
            if (
                self.material(xy_left + XY(0, 1)) in self.PERMEABLE
                or self.material(xy_right + XY(0, 1)) in self.PERMEABLE
            ):
                if xy_left not in flooded_from:
                    to_flood_from.append(xy_left)
                if xy_right not in flooded_from:
                    to_flood_from.append(xy_right)
            else:
                for x in range(xy_left.x, xy_right.x + 1):
                    self.grid[XY(x, xy.y)] = self.STANDING
                self.grid[xy + XY(0, -1)] = self.FLOWING
                to_flood_from.append(xy + XY(0, -1))

    def draw_system(self):
        min_x, max_x = min(xy[0] for xy in self.grid), max(xy[0] for xy in self.grid)
        header = "      " + "".join([str(x % 10) for x in range(min_x, max_x + 1)])
        print(header)
        for y in range(self.bottom + 1):
            print(f"{y:5d} ", end="")
            for x in range(min_x, max_x + 1):
                print(self.material(XY(x, y)), end="")
            print(f" {y:<5d} ")
        print(header)


@print_time_taken
def solve(inputs):
    reservoir = Reservoir(inputs)
    # reservoir.draw_system()
    print(f"Part 1: {sum(v in reservoir.WATER for v in reservoir.grid.values())}")
    print(f"Part 2: {sum(v == reservoir.STANDING for v in reservoir.grid.values()) }\n")


solve(sample_input)
solve(actual_input)
