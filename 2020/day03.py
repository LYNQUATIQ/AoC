import logging
import math
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


def get_trees(right, down):
    y = 0
    trees = 0
    while y < len(lines):
        line = lines[y]
        x = (y // down * right) % len(line)
        if line[x] == "#":
            trees += 1
        y += down
    return trees


print(f"Part 1: {get_trees(3, 1)}")

routes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print(f"Part 2: {math.prod([get_trees(right, down) for right, down in routes])}")
