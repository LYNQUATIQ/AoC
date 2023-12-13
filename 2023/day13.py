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


class NoReflection(Exception):
    """Raised if no relfection found"""


def find_vertical_reflection(pattern: list[str], ignore: int = 0) -> int | None:
    width = len(pattern[0])
    rows = ["".join(row[x] for row in pattern) for x in range(width)]
    return find_horizontal_reflection(rows, ignore)


def find_horizontal_reflection(rows: list[str], ignore: int = 0) -> int | None:
    n_rows = len(rows)
    for y in range(1, n_rows):
        if y == ignore:
            continue
        rows_to_check = min(n_rows - y, y)
        if all(rows[y + i] == rows[y - i - 1] for i in range(rows_to_check)):
            return y
    return None


def solve(inputs: str):
    patterns = [grid.splitlines() for grid in inputs.split("\n\n")]

    vertical_mirrors, horizonatal_mirrors = [], []
    reflection_lines = []
    for pattern in patterns:
        h_mirror = find_horizontal_reflection(pattern)
        if h_mirror:
            reflection_lines.append((0, h_mirror))
            continue
        v_mirror = find_vertical_reflection(pattern)
        assert v_mirror is not None
        reflection_lines.append((v_mirror, 0))
    vertical_mirrors = sum(m[0] for m in reflection_lines)
    horizonatal_mirrors = sum(m[1] for m in reflection_lines)
    print(f"Part 1: {vertical_mirrors + 100 * horizonatal_mirrors}")

    vertical_mirrors, horizonatal_mirrors = [], []
    for i, pattern in enumerate(patterns):
        width, height = len(pattern[0]), len(pattern)
        for x, y in product(range(width), range(height)):
            if i == 5 and y == 2 and x == 8:
                breakpoint()
            corrected_pattern = pattern[:]
            row = pattern[y]
            symbol = ASH if row[x] == ROCK else ROCK
            corrected_pattern[y] = row[:x] + symbol + row[x + 1 :]
            h_mirror = find_horizontal_reflection(
                corrected_pattern, reflection_lines[i][1]
            )
            if h_mirror and reflection_lines[i] != (0, h_mirror):
                horizonatal_mirrors.append(h_mirror)
                print(
                    f"Corrected ({x}, {y}) for pattern {i} - new horizontal reflection: {h_mirror}  vs {reflection_lines[i]}"
                )
            else:
                v_mirror = find_vertical_reflection(
                    corrected_pattern, reflection_lines[i][0]
                )
                if v_mirror and reflection_lines[i] != (v_mirror, 0):
                    vertical_mirrors.append(v_mirror)
                    print(
                        f"Corrected ({x}, {y}) for pattern {i} - new vertical reflection: {v_mirror}  vs {reflection_lines[i]}"
                    )
                else:
                    continue
            break
        else:
            raise RuntimeError(f"No mirror found for pattern {i}")
    print(f"Part 2: {sum(vertical_mirrors) + 100 * sum(horizonatal_mirrors)}\n")


solve(sample_input)
solve(actual_input)
# 33128 is too low
