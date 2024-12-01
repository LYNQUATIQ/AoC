import logging
import os

from itertools import permutations

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_2.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_2_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


rows = []
for line in lines:
    rows.append([int(i) for i in line.split("\t")])

checksum = 0
for row in rows:
    checksum += max(row) - min(row)
print(f"Part 1: {checksum}")

checksum = 0
for row in rows:
    for a, b in permutations(row, 2):
        if a > b and a % b == 0:
            checksum += a // b
            break
print(f"Part 2: {checksum}")
