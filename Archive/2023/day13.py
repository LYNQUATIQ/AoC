"""https://adventofcode.com/2023/day/13"""
import os

from itertools import product

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
UNSMUDGE = {ASH: ROCK, ROCK: ASH}


def find_horizontal_reflection_line(rows: list[str], ignore: int = 0) -> int | None:
    for y in (y for y in range(1, len(rows)) if y != ignore):
        if all(rows[y + i] == rows[y - i - 1] for i in range(min(len(rows) - y, y))):
            return y
    return None


def find_reflection_line(
    pattern: list[str], ignore: tuple[int, int] = (0, 0)
) -> tuple[int, int] | None:
    if h_mirror := find_horizontal_reflection_line(pattern, ignore[1]):
        return (0, h_mirror)
    pattern = ["".join(row[x] for row in pattern) for x in range(len(pattern[0]))]
    if v_mirror := find_horizontal_reflection_line(pattern, ignore[0]):
        return (v_mirror, 0)
    return None


def solve(inputs: str):
    patterns = [grid.splitlines() for grid in inputs.split("\n\n")]
    lines1 = [find_reflection_line(pattern) for pattern in patterns]
    lines2 = []
    for pattern, prior_reflection in zip(patterns, lines1):
        for x, y in product(range(len(pattern[0])), range(len(pattern))):
            pattern2 = pattern[:]
            pattern2[y] = pattern[y][:x] + UNSMUDGE[pattern[y][x]] + pattern[y][x + 1 :]
            if mirror := find_reflection_line(pattern2, ignore=prior_reflection):
                lines2.append(mirror)
                break

    print(f"Part 1: {sum(m[0] for m in lines1) + 100 * sum(m[1] for m in lines1)}")
    print(f"Part 2: {sum(m[0] for m in lines2) + 100 * sum(m[1] for m in lines2)}\n")


solve(sample_input)
solve(actual_input)
