import os
import re


with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()

data, medicine = actual_input.split("\n\n")
replacements = dict((l.split(" => ")[::-1] for l in data.splitlines()))


possible_molecules = set()
for replacement, initial in replacements.items():
    for m in re.finditer(initial, medicine):
        possible_molecules.add(
            medicine[: m.span()[0]] + replacement + medicine[m.span()[1] :]
        )
print(f"Part 1: {len(possible_molecules)}")


class DeadEnd(Exception):
    """Used to indicate dead end"""


DEAD_ENDS = set()
NEXT_STEPS = {}


def path_length(seed, path_so_far=0):
    if seed == "e":
        return path_so_far

    try:
        next_steps = NEXT_STEPS[seed]
    except KeyError:
        next_steps = set()
        for initial, replacement in replacements.items():
            for m in re.finditer(initial, seed):
                next_steps.add(seed[: m.span()[0]] + replacement + seed[m.span()[1] :])
        NEXT_STEPS[seed] = next_steps

    next_steps = sorted((p for p in next_steps if p not in DEAD_ENDS), key=len)
    while next_steps:
        next_step = next_steps.pop(0)
        try:
            return path_length(next_step, path_so_far + 1)
        except DeadEnd:
            DEAD_ENDS.add(next_step)
    raise DeadEnd


print(f"Part 2: {path_length(medicine)}\n")
