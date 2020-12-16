import math
import os

from collections import defaultdict
from itertools import product

from utils import print_time_taken

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()


@print_time_taken
def solve(inputs):
    rule_lines, ticket, nearby = inputs.split("\n\n")

    ticket = list(map(int, ticket.splitlines()[1].split(",")))
    nearby = [list(map(int, line.split(","))) for line in nearby.splitlines()[1:]]
    rules = {}
    for field, bounds in (tuple(line.split(":")) for line in rule_lines.splitlines()):
        rules[field] = set(
            map(lambda x: tuple(map(int, x.split("-"))), bounds.split(" or "))
        )

    possible_indices = {k: set(range(len(rules))) for k in rules}
    part1 = 0
    for values in nearby:
        not_possible = defaultdict(set)
        for index, value in enumerate(values):
            for field, bounds in rules.items():
                if not any((low <= value <= high for low, high in bounds)):
                    not_possible[index].add(field)
        invalid_indices = [i for i, v in not_possible.items() if len(v) == len(rules)]
        if invalid_indices:
            part1 += sum(values[i] for i in invalid_indices)
            continue
        for i, impossible_fields in not_possible.items():
            for field in impossible_fields:
                possible_indices[field].discard(i)
    print(f"Part 1: {part1}")

    indices = {}
    while indices.keys() != rules.keys():
        field, index = next((k, v) for k, v in possible_indices.items() if len(v) == 1)
        indices[field] = index.pop()
        for other_field in possible_indices:
            possible_indices[other_field].discard(indices[field])
    part2 = (ticket[i] for k, i in indices.items() if k.startswith("departure"))
    print(f"Part 2: {math.prod(part2)}\n")


solve(actual_input)
