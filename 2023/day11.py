"""https://adventofcode.com/2023/day/11"""
import os

from itertools import product

with open(os.path.join(os.path.dirname(__file__), "inputs/day11_input.txt")) as f:
    actual_input = f.read()


sample_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def expand_galaxies(inputs: str, expansion: int = 2):
    galaxy_x: dict[int, int] = {}
    galaxy_y: dict[int, int] = {}
    n = 0
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                galaxy_x[n] = x
                galaxy_y[n] = y
                n += 1
    width, height = x + 1, y + 1

    empty_rows = set(y for y in range(height) if y not in galaxy_y.values())
    empty_columns = set(x for x in range(width) if x not in galaxy_x.values())

    for i in range(n):
        x, y = galaxy_x[i], galaxy_y[i]
        galaxy_x[i] += sum([column < x for column in empty_columns]) * (expansion - 1)
        galaxy_y[i] += sum([row < y for row in empty_rows]) * (expansion - 1)

    return n, galaxy_x, galaxy_y


def solve(inputs, expansion: int):
    n, galaxy_x, galaxy_y = expand_galaxies(inputs)
    total = 0
    for g1 in range(n):
        for g2 in range(g1 + 1, n):
            total += abs(galaxy_x[g1] - galaxy_x[g2]) + abs(galaxy_y[g1] - galaxy_y[g2])
    print(f"Part 1: {total}")

    n, galaxy_x, galaxy_y = expand_galaxies(inputs, expansion)
    total = 0
    for g1 in range(n):
        for g2 in range(g1 + 1, n):
            total += abs(galaxy_x[g1] - galaxy_x[g2]) + abs(galaxy_y[g1] - galaxy_y[g2])
    print(f"Part 2: {total}\n")


solve(sample_input, 10)
solve(actual_input, 1_000_000)
