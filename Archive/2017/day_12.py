import logging
import os

import re

from collections import defaultdict


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_12.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/2017_day_12_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

pattern = re.compile(r"^(?P<program>[\d]+) <-> (?P<connections>[\d, ]+)$")

program_groups = {}
groups = {}

for line in lines:
    params = pattern.match(line).groupdict()
    program = int(params["program"])
    connections = [int(c) for c in params["connections"].split(", ")]

    try:
        group = program_groups[program]
    except KeyError:
        group = program
        groups[group] = set([program])
        program_groups[program] = group

    for connection in connections:
        if connection == program:
            continue

        try:
            existing_group = program_groups[connection]
        except KeyError:
            groups[group].add(connection)
            program_groups[connection] = group
            continue

        if existing_group == group:
            continue

        for p in groups[existing_group]:
            groups[group].add(p)
            program_groups[p] = group

        del groups[existing_group]

print(f"Part 1: {len(groups[program_groups[0]])}")
print(f"Part 2: {len(groups)}")

