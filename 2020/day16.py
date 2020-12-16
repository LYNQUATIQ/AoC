import math
import os
from collections import defaultdict
from utils import flatten, print_time_taken

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()


@print_time_taken
def solve(inputs):
    rules_list, your_ticket, nearby_tickets = inputs.split("\n\n")

    rules_list = dict([tuple(line.split(":")) for line in rules_list.split("\n")])
    rules = defaultdict(list)
    for k, v in rules_list.items():
        for valid in v.split(" or "):
            lower, upper = valid.split("-")
            rules[k].append((int(lower), int(upper)))
    all_rules = list(flatten(rules.values()))

    invalid_values, valid_tickets = [], []
    for line in nearby_tickets.split("\n")[1:]:
        is_valid = True
        ticket_values = [int(v) for v in line.split(",")]
        for value in ticket_values:
            if not any((lower <= value <= upper for lower, upper in all_rules)):
                invalid_values.append(value)
                is_valid = False
        if is_valid:
            valid_tickets.append(ticket_values)
    print(f"Part 1: {sum(invalid_values)}")

    possible_indices = {k: set(range(len(rules))) for k in rules}
    for ticket_values in valid_tickets:
        for i, value in enumerate(ticket_values):
            for k, valid_values in rules.items():
                if not any((lower <= value <= upper for lower, upper in valid_values)):
                    possible_indices[k].discard(i)

    field_index = {}
    while len(field_index) < len(rules):
        field, index = [(k, v) for k, v in possible_indices.items() if len(v) == 1][0]
        (index,) = index
        field_index[field] = index
        for field in possible_indices:
            possible_indices[field].discard(index)

    values = [int(v) for v in your_ticket.split("\n")[1].split(",")]
    part2 = (values[i] for k, i in field_index.items() if k.startswith("departure"))
    print(f"Part 2: {math.prod(part2)}\n")


solve(actual_input)
