import os

from itertools import combinations

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

values = [int(line) for line in lines]

PREAMBLE = 25

part1 = None
for i in range(PREAMBLE, len(values)):
    n = values[i]
    sum_of_pairs = set(a + b for a, b in combinations(values[i - PREAMBLE : i], 2))
    if n not in sum_of_pairs:
        part1 = n
        break
print(f"Part 1: {part1}")

part2 = None
for i in range(2, len(values)):
    for j in range(i):
        if sum(values[j:i]) == part1:
            part2 = min(values[j:i]) + max(values[j:i])
            break
    if sum(values[j:i]) >= part1:
        break
print(f"Part 2: {part2}")
