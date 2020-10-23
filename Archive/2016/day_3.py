import logging
import os

import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

pattern = re.compile(r"^\s*(?P<a>\d+)\s+(?P<b>\d+)\s+(?P<c>\d+)$")

valid = 0
for line in lines:
    sides = sorted([int(i) for i in pattern.match(line).groupdict().values()])
    if sides[0] + sides[1] > sides[2]:
        valid += 1

print(f"Part 1: {valid}")

valid = 0
for i in range(0, len(lines), 3):
    rows = []
    for line in lines[i:i+3]:
        rows.append([int(i) for i in pattern.match(line).groupdict().values()])
    for triangle in range(3):
        sides = sorted([rows[0][triangle], rows[1][triangle], rows[2][triangle]])
        if sides[0] + sides[1] > sides[2]:
            valid += 1

print(f"Part 2: {valid}")