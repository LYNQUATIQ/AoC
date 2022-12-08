"""https://adventofcode.com/2022/day/8"""
import os

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
    max_x, max_y = max(xy[0] for xy in grid) + 1, max(xy[1] for xy in grid) + 1

    visible = 0
    scenic_scores = set()

    for (this_x, this_y), height in grid.items():

        if (
            all(grid[(x, this_y)] < height for x in range(this_x))
            or all(grid[(x, this_y)] < height for x in range(this_x + 1, max_x))
            or all(grid[(this_x, y)] < height for y in range(this_y))
            or all(grid[(this_x, y)] < height for y in range(this_y + 1, max_y))
        ):
            visible += 1

        view_left, view_right, view_up, view_down = 0, 0, 0, 0
        for x in range(this_x - 1, -1, -1):
            view_left += 1
            if grid[(x, this_y)] >= height:
                break
        for x in range(this_x + 1, max_x):
            view_right += 1
            if grid[(x, this_y)] >= height:
                break
        for y in range(this_y - 1, -1, -1):
            view_down += 1
            if grid[(this_x, y)] >= height:
                break
        for y in range(this_y + 1, max_y):
            view_up += 1
            if grid[(this_x, y)] >= height:
                break
        scenic_scores.add(view_left * view_right * view_up * view_down)

    print(f"Part 1: {visible}")
    print(f"Part 2: {max(scenic_scores)}\n")


solve(sample_input)
solve(actual_input)
