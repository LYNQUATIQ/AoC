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
        bricks[chr(i + 65)] = (z0, z1, footprint)

    column_bricks = defaultdict(list)
    for xy in product(range(x_range), range(y_range)):
        xy_bricks = [
            (z, brick) for brick, (_, z, footprint) in bricks.items() if xy in footprint
        ]
        column_bricks[xy] = [brick for _, brick in sorted(xy_bricks)]

    # Let the bricks fall
    for this in sorted(bricks, key=bricks.get):
        z0, z1, footprint = bricks[this]
        delta_z, max_z = z1 - z0, {}
        for xy in footprint:
            max_z[xy] = 0
            for b in column_bricks[xy]:
                if b == this:
                    break
                max_z[xy] = bricks[b][1]
        z0 = max(max_z.values()) + 1
        bricks[this] = (z0, z0 + delta_z, footprint)

    # Determine which bricks are below each brick and within their footprint
    bricks_below = {}
    for this, (_, this_z, this_footprint) in bricks.items():
        bricks_below[this] = {
            other
            for other, (_, other_z, other_footprint) in bricks.items()
            if (this_footprint & other_footprint) and (other_z < this_z)
        }

    # Determine which bricks support other bricks
    bricks_supported_by = defaultdict(set)
    bricks_supporting = defaultdict(set)
    for this, (this_z, _, _) in bricks.items():
        for lower_brick in bricks_below[this]:
            _, lower_z1, _ = bricks[lower_brick]
            if this_z == lower_z1 + 1:
                bricks_supporting[this].add(lower_brick)
                bricks_supported_by[lower_brick].add(this)

    # Count the bricks that are not directly (and solely) supporting any other bricks
    can_be_disintegrated = set()
    for this in bricks:
        sole_support = False
        for supported_brick in bricks_supported_by[this]:
            if bricks_supporting[supported_brick] == {this}:
                sole_support = True
        if not sole_support:
            can_be_disintegrated.add(this)
    print(f"Part 1: {len(can_be_disintegrated)}")

    # Determine how many bricks would fall in a chain reaction
    chain_reaction = {}
    for this in bricks:
        this_reaction = {this}
        to_visit = set(bricks_supported_by[this])
        while to_visit:
            supported_brick = to_visit.pop()
            if not (bricks_supporting[supported_brick] - this_reaction):
                this_reaction.add(supported_brick)
                to_visit |= bricks_supported_by[supported_brick]
        chain_reaction[this] = len(this_reaction) - 1
    print(f"Part 2: {sum(chain_reaction.values())}\n")


solve(sample_input)
solve(actual_input)
