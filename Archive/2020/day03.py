import math
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day03_input.txt")) as f:
    actual_input = f.read()

sample_input = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


def solve(inputs):
    rows = inputs.split("\n")

    def count_trees(right, down):
        x, y, trees = 0, 0, 0
        while y < len(rows):
            trees += rows[y][x] == "#"
            x = (x + right) % len(rows[y])
            y += down
        return trees

    routes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    print(f"Part 1: {count_trees(3, 1)}")
    print(f"Part 2: {math.prod([count_trees(*route) for route in routes])}\n")


solve(sample_input)
solve(actual_input)
