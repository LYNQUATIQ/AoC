"""https://adventofcode.com/2022/day/14"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()


sample_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def solve(inputs: str) -> None:

    blockages = set()
    for line in inputs.splitlines():
        points: list[tuple[int, int]] = []
        for p in line.split(" -> "):
            x, y = map(int, p.split(","))
            points.append((x, y))
        for p_0, p_1 in zip(points[:-1], points[1:]):
            if p_1[0] == p_0[0]:
                s = 1 if p_1[1] > p_0[1] else -1
                for y in range(p_0[1], p_1[1] + s, s):
                    blockages.add((p_1[0], y))
            else:
                s = 1 if p_1[0] > p_0[0] else -1
                for x in range(p_0[0], p_1[0] + s, s):
                    blockages.add((x, p_1[1]))
            p_0 = p_1

    sand_units = 0
    sand_source = (500, 0)
    max_y = max(xy[1] for xy in blockages)
    part1_abyss = max_y + 1
    floor = max_y + 2

    x, y = sand_source
    part_1_sand_units = 1
    while True:

        if y > max_y + 1:
            part_1_sand_units = y
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
        if (x, y - 1) == sand_source:
            break
        x, y = sand_source

    print(f"Part 1: {part_1_sand_units}")
    print(f"Part 2: {sand_units}\n")


solve(sample_input)
solve(actual_input)
