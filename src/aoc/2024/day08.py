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
    antennas = defaultdict(list)
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            if c != ".":
                antennas[c].append(complex(x, y))
    max_x, max_y = x + 1, y + 1

    antinodes_part1, antinodes_part2 = set(), set()
    for antenna_positions in antennas.values():
        for a, b in combinations(antenna_positions, 2):
            for antenna_xy, dxy in ((a, a - b), (b, b - a)):
                multiplier, in_range = 0, True
                while in_range:
                    antinode = antenna_xy + (dxy * multiplier)
                    in_range = 0 <= antinode.real < max_x and 0 <= antinode.imag < max_y
                    if in_range:
                        antinodes_part2.add(antinode)
                        if multiplier == 1:
                            antinodes_part1.add(antinode)
                    multiplier += 1

    print(f"Part 1: {len(antinodes_part1)}")
    print(f"Part 2: {len(antinodes_part2)}\n")


solve(example_input)
solve(actual_input)
