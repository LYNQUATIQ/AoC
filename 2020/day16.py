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
    rules_list, ticket, nearby = inputs.split("\n\n")

    rules_list = dict([tuple(line.split(":")) for line in rules_list.split("\n")])
    ticket = [int(v) for v in ticket.split("\n")[1].split(",")]
    nearby = [[int(v) for v in t.split(",")] for t in nearby.split("\n")[1:]]

    rules = defaultdict(list)
    for k, v in rules_list.items():
        for valid in v.split(" or "):
            lower, upper = valid.split("-")
            rules[k].append((int(lower), int(upper)))

    possible_indices = {k: set(range(len(rules))) for k in rules}
    part1 = 0
    for values in nearby:
        not_possible = defaultdict(list)
        for (i, v), (k, valid_values) in product(enumerate(values), rules.items()):
            if not any((lower <= v <= upper for lower, upper in valid_values)):
                not_possible[i].append(k)
        invalid_i = [i for i, v in not_possible.items() if len(v) == len(rules)]
        if invalid_i:
            part1 += sum(values[i] for i in invalid_i)
            continue
        for i, impossible_fields in not_possible.items():
            for field in impossible_fields:
                possible_indices[field].discard(i)
    print(f"Part 1: {part1}")

    field_index = {}
    while len(field_index) < len(rules):
        field, index = next((k, v) for k, v in possible_indices.items() if len(v) == 1)
        (index,) = index
        field_index[field] = index
        for field in possible_indices:
            possible_indices[field].discard(index)
    part2 = (ticket[i] for k, i in field_index.items() if k.startswith("departure"))
    print(f"Part 2: {math.prod(part2)}\n")


solve(actual_input)
