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

    waiting_times = {b - timestamp % b: b for b in buses}
    print(f"Part 1: {(min(waiting_times)) * waiting_times[min(waiting_times)]}")

    # Use Chinese Remainder Theorem to search for answer by sieving
    # en.wikipedia.org/wiki/Chinese_remainder_theorem
    remainders = {k: (k - v) % k for k, v in buses.items()}
    descending_mods = sorted(remainders.keys(), reverse=True)
    delta = descending_mods[0]
    part2 = remainders[delta]
    for mod in descending_mods[1:]:
        while part2 % mod != remainders[mod]:
            part2 += delta
        delta = delta * mod
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
