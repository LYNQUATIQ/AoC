import os
import re

from collections import defaultdict

from utils import grouper, print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/upping_the_ante.txt")) as f:
    actual_input = f.read()


@print_time_taken
def solve(inputs):
    waves = (list(map(int, line.split(","))) for line in inputs.splitlines())
    bits = []
    for wave in waves:
        boundary_crosses = []
        for b1, b2 in zip(wave[:-1], wave[1:]):
            boundary_crosses.append((b1 > 0) != (b2 > 0))
        bits.append(str(int((sum(boundary_crosses) // 10))))

    for char in grouper(bits, 8):
        print(chr(int("".join(char[1:-2]), 3)), end="")

    print()


solve(actual_input)
