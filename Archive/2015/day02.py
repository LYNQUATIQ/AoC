import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day02_input.txt")) as f:
    actual_input = f.read()


def solve(inputs):
    total_area, ribbon = 0, 0
    for line in inputs.splitlines():
        l, w, h = sorted(map(int, line.split("x")))
        total_area += 3 * l * w + 2 * w * h + 2 * l * h
        ribbon += 2 * l + 2 * w + l * w * h

    print(f"Part 1: {total_area}")
    print(f"Part 2: {ribbon}\n")


solve(actual_input)
