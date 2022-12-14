"""https://adventofcode.com/2022/day/14"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()


sample_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def solve(inputs: str) -> None:

    blockages = set()
    for line in inputs.splitlines():
        points = [tuple(map(int, p.split(","))) for p in line.split(" -> ")]
        for (start_x, start_y), (end_x, end_y) in zip(points[:-1], points[1:]):
            if start_x == end_x:
                s = 1 if end_y > start_y else -1
                blockages |= {(end_x, y) for y in range(start_y, end_y + s, s)}
            else:
                s = 1 if end_x > start_x else -1
                blockages |= {(x, end_y) for x in range(start_x, end_x + s, s)}

    floor = max(xy[1] for xy in blockages) + 2
    sand_units, part_1_sand_units = 0, 0

    SAND_SOURCE = (500, 0)
    x, y = SAND_SOURCE
    while True:
        if y > floor - 1 and not part_1_sand_units:
            part_1_sand_units = sand_units

        if y < floor:
            y += 1
            if (x, y) not in blockages:
                continue
            if (x - 1, y) not in blockages:
                x -= 1
                continue
            if (x + 1, y) not in blockages:
                x += 1
                continue

        blockages.add((x, y - 1))
        sand_units += 1
        if (x, y - 1) == SAND_SOURCE:
            break
        x, y = SAND_SOURCE

    print(f"Part 1: {part_1_sand_units}")
    print(f"Part 2: {sand_units}\n")


solve(sample_input)
solve(actual_input)
