"""https://adventofcode.com/2022/day/8"""
import os
from itertools import product

with open(os.path.join(os.path.dirname(__file__), f"inputs/day08_input.txt")) as f:
    actual_input = f.read()


sample_input = """30373
25512
65332
33549
35390"""


def solve(inputs: str) -> None:
    grid = {
        (x, y): int(height)
        for y, line in enumerate(inputs.splitlines())
        for x, height in enumerate(line)
    }
    width, height = (max(xy[0] for xy in grid) + 1, max(xy[1] for xy in grid) + 1)

    visible = 0
    scenic_scores = set()
    for x0, y0 in product(range(width), range(height)):
        this_tree = grid[(x0, y0)]

        if (
            all(grid[(x, y0)] < this_tree for x in range(x0))
            or all(grid[(x, y0)] < this_tree for x in range(x0 + 1, width))
            or all(grid[(x0, y)] < this_tree for y in range(y0))
            or all(grid[(x0, y)] < this_tree for y in range(y0 + 1, height))
        ):
            visible += 1

        view_left, view_right, view_up, view_down = 0, 0, 0, 0
        for x in range(x0 - 1, -1, -1):
            view_left += 1
            if grid[(x, y0)] >= this_tree:
                break
        for x in range(x0 + 1, width):
            view_right += 1
            if grid[(x, y0)] >= this_tree:
                break
        for y in range(y0 - 1, -1, -1):
            view_down += 1
            if grid[(x0, y)] >= this_tree:
                break
        for y in range(y0 + 1, height):
            view_up += 1
            if grid[(x0, y)] >= this_tree:
                break
        scenic_scores.add(view_left * view_right * view_up * view_down)

    print(f"Part 1: {visible}")
    print(f"Part 2: {max(scenic_scores)}\n")


solve(sample_input)
solve(actual_input)
