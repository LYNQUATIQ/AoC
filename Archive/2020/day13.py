import os
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day13_input.txt")) as f:
    actual_input = f.read()

sample_input = """939
7,13,x,x,59,x,31,19"""


@print_time_taken
def solve(inputs):
    lines = inputs.split("\n")
    timestamp = int(lines[0])
    buses = {int(b): i for i, b in enumerate(lines[1].split(",")) if b != "x"}

    waiting_times = {b - timestamp % b: b for b in buses}
    print(f"Part 1: {(min(waiting_times)) * waiting_times[min(waiting_times)]}")

    # Use Chinese Remainder Theorem to search for answer by sieving
    # en.wikipedia.org/wiki/Chinese_remainder_theorem
    remainders = {k: (k - v) % k for k, v in buses.items()}
    delta, solution = 1, 0
    for modulus in remainders:
        while solution % modulus != remainders[modulus]:
            solution += delta
        delta *= modulus
    print(f"Part 2: {solution}")


solve(sample_input)
solve(actual_input)
