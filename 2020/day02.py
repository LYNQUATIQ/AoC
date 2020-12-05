import logging
import os
import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

part1, part2 = 0, 0
for line in lines:
    a, b, c, p = re.match(r"^(\d+)-(\d+) ([a-z]): ([a-z]+)$", line).groups()
    a, b = int(a), int(b)
    part1 += a <= p.count(c) <= b
    part2 += (p[a - 1] == c) + (p[b - 1] == c) == 1

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
