import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
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
