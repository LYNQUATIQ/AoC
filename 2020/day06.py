import logging
import os

import string

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

questions = string.ascii_lowercase

responses = []
for line in lines:
    if not responses or line == "":
        responses.append(defaultdict(list))
        continue
    for q in questions:
        responses[-1][q].append(q in line)

part1, part2 = 0, 0
for group_responses in responses:
    for q in questions:
        part1 += any(group_responses[q])
        part2 += all(group_responses[q])

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")