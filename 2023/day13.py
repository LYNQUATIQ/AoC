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


def find_v_mirror(pattern: list[str], ignore: int = 0) -> int | None:
    rows = ["".join(row[x] for row in pattern) for x in range(len(pattern[0]))]
    return find_h_mirror(rows, ignore)


def find_h_mirror(rows: list[str], ignore: int = 0) -> int | None:
    n_rows = len(rows)
    for y in range(1, n_rows):
        if y == ignore:
            continue
        if all(rows[y + i] == rows[y - i - 1] for i in range(min(n_rows - y, y))):
            return y
    return None


def solve(inputs: str):
    patterns = [grid.splitlines() for grid in inputs.split("\n\n")]

    v_mirrors, h_mirrors, mirrors = [], [], []
    for pattern in patterns:
        if (h_mirror := find_h_mirror(pattern)) is not None:
            mirrors.append((0, h_mirror))
            h_mirrors.append(h_mirror)
        else:
            assert (v_mirror := find_v_mirror(pattern)) is not None
            mirrors.append((v_mirror, 0))
            v_mirrors.append(v_mirror)
    print(f"Part 1: {sum(v_mirrors) + 100 * sum(h_mirrors)}")

    v_mirrors, h_mirrors = [], []
    for pattern, (original_v_mirror, original_h_mirror) in zip(patterns, mirrors):
        columns, rows = len(pattern[0]), len(pattern)
        for x, y in product(range(columns), range(rows)):
            new_pattern = pattern[:]
            exchanged_symbol = {ASH: ROCK, ROCK: ASH}[pattern[y][x]]
            new_pattern[y] = pattern[y][:x] + exchanged_symbol + pattern[y][x + 1 :]
            h_mirror = find_h_mirror(new_pattern, original_h_mirror)
            if (h_mirror := find_h_mirror(new_pattern, original_h_mirror)) is not None:
                h_mirrors.append(h_mirror)
                break
            if (v_mirror := find_v_mirror(new_pattern, original_v_mirror)) is not None:
                v_mirrors.append(v_mirror)
                break
        else:
            raise RuntimeError(f"No mirror found for pattern: {pattern}")
    print(f"Part 2: {sum(v_mirrors) + 100 * sum(h_mirrors)}\n")


solve(sample_input)
solve(actual_input)
