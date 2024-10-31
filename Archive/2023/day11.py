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


def distance(xy1: tuple[int, int], xy2: tuple[int, int]) -> int:
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def solve(inputs: str, expansion: int):
    galaxies = set()
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                galaxies.add((x, y))
    width, height = x + 1, y + 1
    empty_cols = set(y for y in range(height) if y not in {xy[1] for xy in galaxies})
    empty_rows = set(x for x in range(width) if x not in {xy[0] for xy in galaxies})

    expanded_galaxies = {
        (
            x + sum(empty_row < x for empty_row in empty_rows),
            y + sum(empty_col < y for empty_col in empty_cols),
        )
        for x, y in galaxies
    }
    distances = (distance(xy1, xy2) for xy1, xy2 in combinations(expanded_galaxies, 2))
    print(f"Part 1: {sum(distances)}")

    expanded_galaxies = {
        (
            x + sum(empty_row < x for empty_row in empty_rows) * (expansion - 1),
            y + sum(empty_col < y for empty_col in empty_cols) * (expansion - 1),
        )
        for x, y in galaxies
    }
    distances = (distance(xy1, xy2) for xy1, xy2 in combinations(expanded_galaxies, 2))
    print(f"Part 2: {sum(distances)}\n")


solve(sample_input, 10)
solve(actual_input, 1_000_000)
