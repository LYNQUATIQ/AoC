"""https://adventofcode.com/2022/day/14"""
import os
from grid import Grid, XY

with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()


sample_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def build_grid(inputs: str) -> Grid:
    rocks = {}
    for line in inputs.splitlines():
        points: list[XY] = []
        for p in line.split(" -> "):
            x, y = map(int, p.split(","))
            points.append(XY(x, y))
        for p_0, p_1 in zip(points[:-1], points[1:]):
            if p_1.x == p_0.x:
                s = 1 if p_1.y > p_0.y else -1
                for y in range(p_0.y, p_1.y + s, s):
                    rocks[XY(p_1.x, y)] = "#"
            else:
                s = 1 if p_1.x > p_0.x else -1
                for x in range(p_0.x, p_1.x + s, s):
                    rocks[XY(x, p_1.y)] = "#"
            p_0 = p_1
    grid = Grid()
    grid._grid = rocks
    return grid


def solve(inputs: str) -> None:

    grid = build_grid(inputs)

    sand_units = 0
    sand_source = XY(500, 0)
    part1_abyss = grid.limits[3] + 1
    floor = part1_abyss + 1

    x, y = sand_source
    part_1_sand_units = 1
    while True:

        if y > part1_abyss:
            part_1_sand_units = y
        if y < floor:
            y += 1
            if XY(x, y) not in grid._grid:
                continue
            if XY(x - 1, y) not in grid._grid:
                x -= 1
                continue
            if XY(x + 1, y) not in grid._grid:
                x += 1
                continue
        grid[XY(x, y - 1)] = "o"
        sand_units += 1
        if XY(x, y - 1) == sand_source:
            break
        x, y = sand_source
        # grid.print_grid(show_headers=False)

    print(f"Part 1: {part_1_sand_units}")
    print(f"Part 2: {sand_units}\n")


solve(sample_input)
solve(actual_input)
