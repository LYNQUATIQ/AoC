import os
import string

from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day06_input.txt")) as f:
    actual_input = f.read()

sample_input = """
abc

a
b
c

ab
ac

a
a
a
a

b"""


def solve(inputs, questions=string.ascii_lowercase):
    responses = []
    for line in inputs.split("\n"):
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
    print(f"Part 2: {part2}\n")


solve(sample_input, "abc")
solve(actual_input)
