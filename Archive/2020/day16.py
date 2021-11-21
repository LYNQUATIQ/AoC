import math
import os

from collections import defaultdict
from itertools import product

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day16_input.txt")) as f:
    actual_input = f.read()


@print_time_taken
def solve(inputs):
    field_rules, my_ticket, nearby = inputs.split("\n\n")

    my_ticket = list(map(int, my_ticket.splitlines()[1].split(",")))
    nearby = [list(map(int, line.split(","))) for line in nearby.splitlines()[1:]]
    fields = {}
    for field, rules in (tuple(line.split(":")) for line in field_rules.splitlines()):
        fields[field] = set(
            map(lambda x: tuple(map(int, x.split("-"))), rules.split(" or "))
        )

    part1 = 0
    possible_fields = {i: set(fields.keys()) for i in range(len(fields))}
    for values in nearby:
        bad_fields = defaultdict(set)
        for (i, value), (field, rules) in product(enumerate(values), fields.items()):
            if not any((low <= value <= high for low, high in rules)):
                bad_fields[i].add(field)
        bad_values = [values[i] for i, v in bad_fields.items() if v == set(fields)]
        if not bad_values:
            for i, impossible_fields in bad_fields.items():
                possible_fields[i] -= impossible_fields
        part1 += sum(bad_values)
    print(f"Part 1: {part1}")

    field_idx = {}
    while set(field_idx) != set(fields):
        bingoes = ((k, v.pop()) for k, v in possible_fields.items() if len(v) == 1)
        index, field = next(bingoes)
        field_idx[field] = index
        for other in possible_fields:
            possible_fields[other].discard(field)

    part2 = (my_ticket[i] for k, i in field_idx.items() if k.startswith("departure"))
    print(f"Part 2: {math.prod(part2)}\n")


solve(actual_input)
