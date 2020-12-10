import os

from collections import Counter

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
values = [int(line) for line in open(input_file)]

SEAT = 0
DEVICE = max(values) + 3
adapters = [DEVICE] + sorted(values, reverse=True) + [SEAT]

diffs = [a - b for a, b in zip(adapters[:-1], adapters[1:])]
print(f"Part 1: {Counter(diffs)[1] * Counter(diffs)[3]}")

ways_from = {DEVICE: 1}
for n, a in enumerate(adapters[1:], 1):
    next_in_reach = (next_a for next_a in adapters[:n] if next_a - a <= 3)
    ways_from[a] = sum(ways_from[next_a] for next_a in next_in_reach)
print(f"Part 2: {ways_from[SEAT]}")
