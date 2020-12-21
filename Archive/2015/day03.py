import os

from grid_system import XY

with open(os.path.join(os.path.dirname(__file__), f"inputs/day03_input.txt")) as f:
    actual_input = f.read()

sample_input = """^v^v^v^v^v"""


def deliver_presents(inputs, use_robo_santa=False):
    DIRECTIONS = {"<": XY(-1, 0), "^": XY(0, -1), "v": XY(0, 1), ">": XY(1, 0)}

    houses, santa_xy = set(), XY(0, 0)
    houses.add(santa_xy)
    robo_xy = santa_xy
    for i, c in enumerate(inputs):
        if use_robo_santa and i % 2:
            robo_xy += DIRECTIONS[c]
            houses.add(robo_xy)
        else:
            santa_xy += DIRECTIONS[c]
            houses.add(santa_xy)
    return len(houses)


def solve(inputs):
    print(f"Part 1: {deliver_presents(inputs)}")
    print(f"Part 2: {deliver_presents(inputs, use_robo_santa=True)}\n")


solve(sample_input)
solve(actual_input)
