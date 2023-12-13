"""https://adventofcode.com/2023/day/13"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day13_input.txt")) as f:
    actual_input = f.read()


sample_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

ASH, ROCK = ".", "#"


class NoReflection(Exception):
    """Raised if no relfection found"""


def find_vertical_reflection(pattern: list[str]) -> int:
    width = len(pattern[0])
    rows = ["".join(row[x] for row in pattern) for x in range(width)]
    return find_horizontal_reflection(rows)


def find_horizontal_reflection(rows: list[str]) -> int:
    n_rows = len(rows)
    for y in range(1, n_rows):
        rows_to_check = min(n_rows - y, y)
        if all(rows[y + i] == rows[y - i - 1] for i in range(rows_to_check)):
            return y
    raise NoReflection


def solve(inputs: str):
    patterns = [grid.splitlines() for grid in inputs.split("\n\n")]

    vertical_mirrors, horizonatal_mirrors = [], []
    for pattern in patterns:
        try:
            horizonatal_mirrors.append(find_horizontal_reflection(pattern))
        except NoReflection:
            vertical_mirrors.append(find_vertical_reflection(pattern))

    print(f"Part 1: {sum(vertical_mirrors) + 100 * sum(horizonatal_mirrors)}")
    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
