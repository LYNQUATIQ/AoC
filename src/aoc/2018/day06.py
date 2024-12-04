"""https://adventofcode.com/2018/day/6"""

from collections import defaultdict
import os
import sys

from itertools import product


with open(os.path.join(os.path.dirname(__file__), "inputs/day06_input.txt")) as f:
    actual_input = f.read()

example_input = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""


def solve(inputs, d_range):
    coords = {tuple(map(int, line.split(", "))) for line in inputs.splitlines()}
    min_x, min_y = min(c[0] for c in coords), min(c[1] for c in coords)
    max_x, max_y = max(c[0] for c in coords) + 1, max(c[1] for c in coords) + 1

    distances, closest_points = defaultdict(dict), {}
    for x, y in product(range(min_x, max_x), range(min_y, max_y)):
        for xc, yc in coords:
            distances[(x, y)][(xc, yc)] = abs(x - xc) + abs(y - yc)
        shortest_distance, closest = sys.maxsize, None
        for coord, distance in distances[(x, y)].items():
            if distance < shortest_distance:
                shortest_distance, closest = distance, coord
            elif distance == shortest_distance:
                closest = None
        closest_points[(x, y)] = closest

    infinite_areas = set()
    infinite_areas.update(closest_points[min_x, y] for y in range(min_y, max_y))
    infinite_areas.update(closest_points[max_x - 1, y] for y in range(min_y, max_y))
    infinite_areas.update(closest_points[x, min_y] for y in range(min_x, max_x))
    infinite_areas.update(closest_points[x, max_y - 1] for y in range(min_x, max_x))

    areas = {
        coord: sum(v == coord for v in closest_points.values())
        for coord in coords
        if coord not in infinite_areas
    }
    print(f"Part 1: {max(areas.values())}")
    print(f"Part 2: {sum(sum(v.values()) < d_range for v in distances.values())}\n")


solve(example_input, 32)
solve(actual_input, 10000)
