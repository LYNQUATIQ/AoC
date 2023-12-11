"""https://adventofcode.com/2023/day/11"""
import os

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


def expand_galaxies(inputs: str, expansion: int = 2) -> tuple[list[int], list[int]]:
    initial_x, initial_y = [], []
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                initial_x.append(x)
                initial_y.append(y)
    width, height = x + 1, y + 1

    empty_rows = set(y for y in range(height) if y not in initial_y)
    empty_columns = set(x for x in range(width) if x not in initial_x)

    expanded_x, expanded_y = [], []
    for x, y in zip(initial_x, initial_y):
        expanded_x.append(x + (sum([c < x for c in empty_columns]) * (expansion - 1)))
        expanded_y.append(y + (sum([r < y for r in empty_rows]) * (expansion - 1)))

    return expanded_x, expanded_y


def solve(inputs, expansion: int):
    galaxy_x, galaxy_y = expand_galaxies(inputs)
    total = 0
    for g1 in range(len(galaxy_x)):
        for g2 in range(g1 + 1, len(galaxy_x)):
            total += abs(galaxy_x[g1] - galaxy_x[g2]) + abs(galaxy_y[g1] - galaxy_y[g2])
    print(f"Part 1: {total}")

    galaxy_x, galaxy_y = expand_galaxies(inputs, expansion)
    total = 0
    for g1 in range(len(galaxy_x)):
        for g2 in range(g1 + 1, len(galaxy_x)):
            total += abs(galaxy_x[g1] - galaxy_x[g2]) + abs(galaxy_y[g1] - galaxy_y[g2])
    print(f"Part 2: {total}\n")


solve(sample_input, 10)
solve(actual_input, 1_000_000)
