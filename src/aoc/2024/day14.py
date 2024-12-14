"""https://adventofcode.com/2024/day/14"""

import math
import re
import statistics

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


def find_xmas_tree(
    initial_robots: list[tuple[int, int, int, int]], width: int, height: int
):
    # Run through the robot positions unitl they cycle again and note the x/y variances
    robots = initial_robots[:]
    x_variances, y_variances = {}, {}
    for i in range(max(width, height)):
        robots = move_robots(robots, width, height)
        x, y, _, _ = zip(*robots)
        x_variances[i] = statistics.stdev(x)
        y_variances[i] = statistics.stdev(y)

    # Find the iteration with the lowest variance for the x and y positions respectively
    # (the assumption is that the robots will will cluster when they form the xmas tree)
    x_iteration = min(x_variances, key=x_variances.get)
    y_iteration = min(y_variances, key=y_variances.get)

    # Find the subsequent iterations where they hit their 'tree positions' and find the
    # iteration where they hit in both the x and y dimension simultaneously
    x_hits = {x_iteration + width * i for i in range(height)}
    y_hits = {y_iteration + height * i for i in range(width)}
    iterations = (x_hits & y_hits).pop() + 1

    # Draw the xmas tree
    robots = initial_robots
    grid = {(x, y) for x, y, _, _ in move_robots(robots, width, height, iterations)}
    for y in range(height):
        for x in range(width):
            print("*" if (x, y) in grid else " ", end="")
        print()

    print(f"Part 2: {iterations}\n")


def move_robots(
    robots: list[tuple[int, int, int, int]],
    width: int,
    height: int,
    iterations: int = 1,
) -> list[tuple[int, int, int, int]]:
    return [
        ((px + vx * iterations) % width, (py + vy * iterations) % height, vx, vy)
        for px, py, vx, vy in robots
    ]


def solve(inputs: str, width: int, height: int, find_easter_egg: bool = False):
    robots = [tuple(map(int, re.findall(r"-?\d+", m))) for m in inputs.splitlines()]

    final_positions = move_robots(robots, width, height, 100)
    mid_x, mid_y = width // 2, height // 2
    quadrants = defaultdict(int)
    for x, y, _, _ in final_positions:
        if x == mid_x or y == mid_y:
            continue
        quadrants[(y < mid_y, x < mid_x)] += 1

    print(f"Part 1: {math.prod(quadrants.values())}")

    if find_easter_egg:
        find_xmas_tree(robots, width, height)


solve(example_input, 11, 7)
solve(actual_input, 101, 103, find_easter_egg=True)
