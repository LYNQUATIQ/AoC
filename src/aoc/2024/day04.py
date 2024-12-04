"""https://adventofcode.com/2024/day/4"""

from itertools import product

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 4)


sample_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]


def solve(inputs: str):
    grid = inputs.splitlines()
    width, height = len(grid[0]), len(grid)

    def c_at_xy(x: int, y: int) -> str:
        if 0 <= x < width and 0 <= y < height:
            return grid[y][x]
        return ""

    xmas_count = 0
    mas_count = 0
    for x, y in product(range(width), range(height)):
        for dx, dy in DIRECTIONS:
            if all(
                [
                    c_at_xy(y + d * dy, x + d * dx) == c_to_match
                    for c_to_match, d in zip("XMAS", range(4))
                ]
            ):
                xmas_count += 1
        if c_at_xy(x, y) == "A":
            if (
                (c_at_xy(x - 1, y - 1) == "M" and c_at_xy(x + 1, y + 1) == "S")
                or (c_at_xy(x - 1, y - 1) == "S" and c_at_xy(x + 1, y + 1) == "M")
            ) and (
                (c_at_xy(x - 1, y + 1) == "M" and c_at_xy(x + 1, y - 1) == "S")
                or (c_at_xy(x - 1, y + 1) == "S" and c_at_xy(x + 1, y - 1) == "M")
            ):
                mas_count += 1

    print(f"Part 1: {xmas_count}")
    print(f"Part 2: {mas_count}\n")


solve(sample_input)
solve(actual_input)
