"""https://adventofcode.com/2021/day/25"""
# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter
from dataclasses import dataclass, field
from itertools import product

from grid import XY, ConnectedGrid
from utils import flatten, grouper, powerset, print_time_taken

# log_file = os.path.join(os.path.dirname(__file__), f"logs/day25.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
with open(os.path.join(os.path.dirname(__file__), f"inputs/day25_input.txt")) as f:
    actual_input = f.read()

sample_input = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

EAST, SOUTH = ">", "v"


@print_time_taken
def solve(inputs):
    east, south = set(), set()

    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == EAST:
                east.add((x, y))
            if c == SOUTH:
                south.add((x, y))
    width, height = x + 1, y + 1
    steps = 0
    while True:
        steps += 1
        moved = False
        new_east = set()
        for x, y in east:
            xy, target_xy = (x, y), ((x + 1) % width, y)
            if not (target_xy in east or target_xy in south):
                xy, moved = target_xy, True
            new_east.add(xy)
        east = new_east
        new_south = set()
        for x, y in south:
            xy, target_xy = (x, y), (x, (y + 1) % height)
            if not (target_xy in east or target_xy in south):
                xy, moved = target_xy, True
            new_south.add(xy)
        south = new_south

        if not moved:
            break

    print(f"Part 1: {steps}\n")


solve(sample_input)
solve(actual_input)
