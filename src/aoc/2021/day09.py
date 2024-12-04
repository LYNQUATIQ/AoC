"""https://adventofcode.com/2021/day/9"""

import math
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day09_input.txt")) as f:
    actual_input = f.read()

example_input = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def solve(inputs):
    lava_map = {
        (x, y): int(height)
        for y, line in enumerate(inputs.splitlines())
        for x, height in enumerate(line)
    }

    get_neighbours = lambda x, y: ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))

    low_points = []
    for xy, height in lava_map.items():
        if all(lava_map.get(n, 9) > height for n in get_neighbours(*xy)):
            low_points.append(xy)
    print(f"Part 1: {sum(lava_map[low_point]+1 for low_point in low_points)}")

    basin_sizes = []
    for low_point in low_points:
        basin, to_visit = {low_point}, {low_point}
        while to_visit:
            xy = to_visit.pop()
            for neighbour in get_neighbours(*xy):
                if neighbour not in basin and lava_map.get(neighbour, 9) != 9:
                    basin.add(neighbour)
                    to_visit.add(neighbour)
        basin_sizes.append(len(basin))
    print(f"Part 2: {math.prod(sorted(basin_sizes)[-3:])}\n")


solve(example_input)
solve(actual_input)
