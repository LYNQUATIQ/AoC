import math
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """939
7,13,x,x,59,x,31,19"""


def solve(inputs):
    lines = inputs.split("\n")
    timestamp = int(lines[0])
    buses = {int(b): i for i, b in enumerate(lines[1].split(",")) if b != "x"}

    best_b, best_t = None, None
    for b in buses:
        t = math.ceil(timestamp / b) * b
        if best_b is None or (t - timestamp) < best_t:
            best_b = b
            best_t = t - timestamp
    print(f"Part 1: {(best_t)*best_b}")

    mods = {k: (k - v) % k for k, v in buses.items()}
    descending_mods = sorted(mods.keys(), reverse=True)
    delta = descending_mods[0]
    part2 = mods[delta]
    for mod in descending_mods[1:]:
        diff = mods[mod]
        while part2 % mod != diff:
            part2 += delta
        delta = delta * mod
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
