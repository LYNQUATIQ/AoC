import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

from itertools import combinations

values = [int(line) for line in lines]

for a, b in combinations(values, 2):
    if a + b == 2020:
        print(f"Part 1: {a * b}")
        break

for a, b, c in combinations(values, 3):
    if a + b + c == 2020:
        print(f"Part 2: {a * b * c}")
        break
