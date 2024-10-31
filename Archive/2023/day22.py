"""https://adventofcode.com/2023/day/22"""
import os
import re

from collections import defaultdict
from itertools import product

with open(os.path.join(os.path.dirname(__file__), "inputs/day22_input.txt")) as f:
    actual_input = f.read()


sample_input = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


def solve(inputs: str):
    bricks = {}
    x_range, y_range = 0, 0
    for i, line in enumerate(inputs.splitlines()):
        x0, y0, z0, x1, y1, z1 = map(int, re.findall(r"\d+", line))
        x_range, y_range = max(x_range, x1 + 1), max(y_range, y1 + 1)
        footprint = {xy for xy in product(range(x0, x1 + 1), range(y0, y1 + 1))}
        bricks[i] = (z0, z1, footprint)

    # Determine which bricks are below each brick (within their footprint)
    bricks_below = {}
    for this_brick, (_, this_z, this_footprint) in bricks.items():
        bricks_below[this_brick] = {
            other
            for other, (_, other_z, other_footprint) in bricks.items()
            if (this_footprint & other_footprint) and (other_z < this_z)
        }

    # Let the bricks fall - starting from the bottom and working up
    for this_brick in sorted(bricks, key=bricks.get):
        z0, z1, footprint = bricks[this_brick]
        delta_z, z0 = z1 - z0, 1
        for other in bricks_below[this_brick]:
            z0 = max(z0, bricks[other][1] + 1)
        bricks[this_brick] = (z0, z0 + delta_z, footprint)

    # Determine which bricks support which other bricks
    bricks_supported_by = defaultdict(set)
    bricks_supporting = defaultdict(set)
    for this_brick, (this_z, _, _) in bricks.items():
        for lower_brick in bricks_below[this_brick]:
            if this_z == bricks[lower_brick][1] + 1:
                bricks_supporting[this_brick].add(lower_brick)
                bricks_supported_by[lower_brick].add(this_brick)

    # Count the bricks that are not directly (and solely) supporting any other bricks
    can_be_disintegrated = set()
    for this_brick in bricks:
        sole_support = False
        for supported_brick in bricks_supported_by[this_brick]:
            if bricks_supporting[supported_brick] == {this_brick}:
                sole_support = True
        if not sole_support:
            can_be_disintegrated.add(this_brick)
    print(f"Part 1: {len(can_be_disintegrated)}")

    # Determine how many bricks would fall in a chain reaction
    chain_reaction = {}
    for this_brick in bricks:
        this_reaction = {this_brick}
        to_visit = set(bricks_supported_by[this_brick])
        while to_visit:
            supported_brick = to_visit.pop()
            if not (bricks_supporting[supported_brick] - this_reaction):
                this_reaction.add(supported_brick)
                to_visit |= bricks_supported_by[supported_brick]
        chain_reaction[this_brick] = len(this_reaction) - 1
    print(f"Part 2: {sum(chain_reaction.values())}\n")


solve(sample_input)
solve(actual_input)
