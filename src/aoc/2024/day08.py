"""https://adventofcode.com/2024/day/8"""

from collections import defaultdict
from itertools import combinations

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 8)


example_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def solve(inputs: str):
    ants = defaultdict(lambda: list)
    ants = {}
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            xy = complex(x, y)
            if c != ".":
                try:
                    ants[c].append(xy)
                except KeyError:
                    ants[c] = [xy]
    height, width = y + 1, x + 1

    antinodes = set()
    for positions in ants.values():
        for a, b in combinations(positions, 2):
            in_range = True
            i = 0
            dxy = b - a
            antinodes.add(a)
            antinodes.add(b)
            while in_range:
                a0 = a - (dxy * i)
                i += 1
                in_range = False
                if 0 <= a0.real < width and 0 <= a0.imag < height:
                    antinodes.add(a0)
                    in_range = True

                a0 = b + (dxy * i)
                if 0 <= a0.real < width and 0 <= a0.imag < height:
                    antinodes.add(a0)
                    in_range = True

    print(f"Part 1: {len(antinodes)}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
