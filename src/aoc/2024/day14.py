"""https://adventofcode.com/2024/day/14"""

import re
from collections import defaultdict

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 14)


example_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


ITERATIONS = 100


def solve(inputs: str, width: int, height: int):
    robots = [tuple(map(int, re.findall(r"-?\d+", m))) for m in inputs.splitlines()]

    positions = []
    for px, py, vx, vy in robots:
        x = (px + vx * ITERATIONS) % width
        y = (py + vy * ITERATIONS) % height
        positions.append((x, y))

    mid_x, mid_y = width // 2, height // 2
    quadrants = defaultdict(int)
    grid = defaultdict(int)
    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue
        in_top, in_left = y < mid_y, x < mid_x
        quadrants[(in_top, in_left)] += 1

    # Multiply together the values of quadrants
    rating = 1
    for value in quadrants.values():
        rating *= value

    # iteration == 0
    # while True:
    # for y in range(height):
    #     for x in range(width):
    #         n = grid[(x, y)]
    #         c = "." if n == 0 else int(n)
    #         if x == mid_x or y == mid_y:
    #             c = " "
    #         print(c, end="")
    #     print()
    # input()

    print(f"Part 1: {rating}")
    print(f"Part 2: {False}\n")


solve(example_input, 11, 7)
solve(actual_input, 101, 103)
