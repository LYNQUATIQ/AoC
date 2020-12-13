import os

import itertools as it

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def solve(inputs, preamble=25):
    values = [int(line) for line in inputs.split("\n")]

    part1 = None
    for i in range(preamble, len(values)):
        n = values[i]
        sum_of_pairs = set(
            a + b for a, b in it.combinations(values[i - preamble : i], 2)
        )
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
    print(f"Part 2: {part2}\n")


solve(sample_input, 5)
solve(actual_input)
