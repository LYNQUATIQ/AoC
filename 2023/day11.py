"""https://adventofcode.com/2023/day/11"""
import os

from itertools import combinations

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


def expand_galaxies(inputs: str, expansion: int = 2) -> set[tuple[int, int]]:
    initial = set()
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                initial.add((x, y))
    width, height = x + 1, y + 1
    empty_rows = set(y for y in range(height) if y not in {xy[1] for xy in initial})
    empty_columns = set(x for x in range(width) if x not in {xy[0] for xy in initial})

    return {
        (
            x + sum([column < x for column in empty_columns]) * (expansion - 1),
            y + sum([row < y for row in empty_rows]) * (expansion - 1),
        )
        for x, y in initial
    }


def solve(inputs: str, expansion: int):
    galaxies = expand_galaxies(inputs)
    distances = [
        abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in combinations(galaxies, 2)
    ]
    print(f"Part 1: {sum(distances)}")

    galaxies = expand_galaxies(inputs, expansion)
    distances = [
        abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in combinations(galaxies, 2)
    ]
    print(f"Part 2: {sum(distances)}\n")


solve(sample_input, 10)
solve(actual_input, 1_000_000)
