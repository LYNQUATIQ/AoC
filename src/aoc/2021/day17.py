"""https://adventofcode.com/2021/day/17"""

import re
from itertools import product

example_input = """target area: x=20..30, y=-10..-5"""
actual_input = """target area: x=96..125, y=-144..-98"""


def solve(inputs):

    left, right, bottom, top = map(int, re.findall(r"-?\d+", inputs))

    # The highest shot will be the one that hits the water and in the *next* step hits
    # the bottom of the target. It hits the water at the same velocity it rose at, so
    # the velocity needs to equal the (absolute) depth (will also be the max velocity)

    print(f"Part 1: {sum(range(abs(bottom)))}")

    valid_velocities = 0
    for vx, vy in product(range(1, right + 1), range(bottom, abs(bottom) + 1)):
        x, y = 0, 0
        while y >= bottom:
            x, y = x + vx, y + vy
            vx, vy = max(vx - 1, 0), vy - 1
            if left <= x <= right and bottom <= y <= top:
                valid_velocities += 1
                break

    print(f"Part 2: {valid_velocities}\n")


solve(example_input)
solve(actual_input)
