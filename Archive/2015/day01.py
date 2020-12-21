import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day01_input.txt")) as f:
    actual_input = f.read()


def solve(inputs):
    line = inputs.splitlines()[0]

    floor, basement_entry_i = 0, None
    for i, c in enumerate(inputs, 1):
        if c == "(":
            floor += 1
        else:
            floor -= 1
        if basement_entry_i is None and floor == -1:
            basement_entry_i = i

    print(f"Part 1: {floor}")
    print(f"Part 2: {basement_entry_i}\n")


solve(actual_input)
