import logging
import os

from collections import Counter
from itertools import combinations

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_4.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_4_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


valid = 0
for line in lines:
    passphrase = line.split(" ")
    if len(passphrase) != len(set(passphrase)):
        continue
    valid += 1

print(f"Part 1: {valid}")


valid = 0
for line in lines:
    passphrase = line.split(" ")
    invalid = False
    for a, b in combinations(passphrase, 2):
        if Counter(a) == Counter(b):
            invalid = True
    if invalid:
        continue
    valid += 1

print(f"Part 2: {valid}")
