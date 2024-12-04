"""https://adventofcode.com/2024/day/4"""

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

    def get_c(x, y):
        if 0 <= x < width and 0 <= y < height:
            return grid[y][x]
        return ""

    xmas_count = 0
    mas_count = 0
    for x in range(width):
        for y in range(height):
            for dx, dy in DIRECTIONS:
                found_xmas = True
                for c, i in zip("XMAS", range(4)):
                    if get_c(y + i * dy, x + i * dx) != c:
                        found_xmas = False
                        break
                if found_xmas:
                    xmas_count += 1
            if get_c(x, y) == "A":
                if (
                    (get_c(x - 1, y - 1) == "M" and get_c(x + 1, y + 1) == "S")
                    or (get_c(x - 1, y - 1) == "S" and get_c(x + 1, y + 1) == "M")
                ) and (
                    (get_c(x - 1, y + 1) == "M" and get_c(x + 1, y - 1) == "S")
                    or (get_c(x - 1, y + 1) == "S" and get_c(x + 1, y - 1) == "M")
                ):
                    mas_count += 1

    print(f"Part 1: {xmas_count}")
    print(f"Part 2: {mas_count}\n")


solve(sample_input)
solve(actual_input)
