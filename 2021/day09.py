import math
import os

from grid import XY
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day09_input.txt")) as f:
    actual_input = f.read()

sample_input = """2199943210
3987894921
9856789892
8767896789
9899965678"""


@print_time_taken
def solve(inputs):
    lava_map = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, height in enumerate(line):
            lava_map[XY(x, y)] = int(height)

    low_points, risk_levels = [], []
    for xy, height in lava_map.items():
        if all(lava_map.get(n, 9) > height for n in xy.neighbours):
            low_points.append(xy)
            risk_levels.append(height + 1)
    print(f"Part 1: {sum(risk_levels)}")

    basins = []
    for low_point in low_points:
        basin, to_visit = {low_point}, {low_point}
        while to_visit:
            for n in to_visit.pop().neighbours:
                if n not in basin and n in lava_map and lava_map[n] != 9:
                    basin.add(n)
                    to_visit.add(n)
        basins.append(len(basin))
    basins.sort(reverse=True)
    print(f"Part 2: {math.prod(basins[:3])}\n")


solve(sample_input)
solve(actual_input)
