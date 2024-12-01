import logging
import os

import re
import string

from collections import Counter, defaultdict


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

characters = defaultdict(list)
for line in lines:
    for i, c in enumerate(line):
        characters[i].append(c)

part1 = ""
part2 = ""
for p in sorted(characters.keys()):
    part1 += Counter(characters[p]).most_common(1)[0][0]
    part2 += Counter(characters[p]).most_common()[-1][0]

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
