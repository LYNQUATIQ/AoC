import math
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


def count_trees(right, down):
    x, y, trees = 0, 0, 0
    while y < len(lines):
        trees += lines[y][x] == "#"
        x = (x + right) % len(lines[y])
        y += down
    return trees


routes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

print(f"Part 1: {count_trees(3, 1)}")
print(f"Part 2: {math.prod([count_trees(*route) for route in routes])}")
