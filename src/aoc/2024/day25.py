"""https://adventofcode.com/2024/day/25"""

from itertools import product

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 25)
example_input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


def solve(inputs: str):
    locks, keys = [], []
    for schematic in inputs.split("\n\n"):
        lines = schematic.split("\n")
        heights = [sum(c == "#" for c in column) for column in list(zip(*lines))]
        if lines[0].startswith("#"):
            locks.append(heights)
        else:
            keys.append(heights)

    fit_count = 0
    for lock, key in product(keys, locks):
        if all(key[pin] + lock[pin] <= 7 for pin in range(5)):
            fit_count += 1
    print(f"Part 1: {fit_count}\n")


solve(example_input)
solve(actual_input)
