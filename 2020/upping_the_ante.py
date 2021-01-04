import os
import re

from collections import defaultdict

from utils import grouper, print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/upping_the_ante.txt")) as f:
    actual_input = f.read()


@print_time_taken
def solve(inputs):
    values = (list(map(int, line.split(","))) for line in inputs.splitlines())
    bits = []
    for bit in values:
        wave = [b > 0 for b in bit]
        sequences, i = [], 0
        while i < (len(wave) - 1):
            c = 0
            i += 1
            while wave[i] == wave[i + 1]:
                i += 1
                c += 1
                if i >= (len(wave) - 1):
                    break
            sequences.append(c)
        bits.append(str(int(2 - (sum(sequences) / len(sequences)) // 3)))

    for char in grouper(bits, 8):
        print(chr(int("".join(char[1:-2]), 3)), end="")

    print()


solve(actual_input)
