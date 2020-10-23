import logging
import os

from collections import defaultdict
from itertools import combinations

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

containers = [int(line) for line in lines]

good_combos = defaultdict(int)
for i in range(1, len(containers) + 1):
    for combo in combinations(containers, i):
        if sum(combo) == 150:
            good_combos[len(combo)] += 1

print(f"Part 1: {sum(good_combos.values())}")
print(f"Part 2: {good_combos[min(good_combos.keys())]}")