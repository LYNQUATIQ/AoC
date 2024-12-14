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


def solve(inputs: str, width: int, height: int):
    robots = [tuple(map(int, re.findall(r"-?\d+", m))) for m in inputs.splitlines()]

    final_positions = []
    for px, py, vx, vy in robots:
        x = (px + vx * 100) % width
        y = (py + vy * 100) % height
        final_positions.append((x, y))

    mid_x, mid_y = width // 2, height // 2
    quadrants = defaultdict(int)
    for x, y in final_positions:
        if x == mid_x or y == mid_y:
            continue
        quadrants[(y < mid_y, x < mid_x)] += 1

    safety_factor = 1
    for value in quadrants.values():
        safety_factor *= value
    print(f"Part 1: {safety_factor}")


def find_xmas_tree(inputs: str, width: int, height: int):
    robots = [tuple(map(int, re.findall(r"-?\d+", m))) for m in inputs.splitlines()]
    iteration, interesting = 0, False
    while not interesting:
        iteration += 1
        new_robots = []
        grid = defaultdict(lambda: False)
        rows, columns = defaultdict(int), defaultdict(int)
        for px, py, vx, vy in robots:
            x = (px + vx) % width
            y = (py + vy) % height
            grid[(x, y)] = True
            columns[x] += 1
            rows[y] += 1
            new_robots.append((x, y, vx, vy))
        robots = new_robots
        interesting = max(rows.values()) > 30 and max(columns.values()) > 30

    for y in range(height):
        for x in range(width):
            print("*" if grid[(x, y)] else " ", end="")
        print()
    print(f"Part 2: {iteration}\n")


solve(example_input, 11, 7)
solve(actual_input, 101, 103)
find_xmas_tree(actual_input, 101, 103)
