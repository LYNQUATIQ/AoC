import os
import re

from collections import defaultdict

from utils import grouper, print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/upping_the_ante.txt")) as f:
    actual_input = f.read()


@print_time_taken
def solve(inputs):
    # values = []
    # for line in inputs.splitlines():
    #     print(line)
    #     values.append([int(x) for x in line.split(",")])
    values = (list(map(int, line.split(","))) for line in inputs.splitlines())
    bits = []
    for bit in values:
        wave = [b > 0 for b in bit]
        sequences, i = [], 0
        while wave[i] == wave[i + 1]:
            i += 1
        while True:
            c = 0
            i += 1
            if i >= (len(wave) - 1):
                break
            while wave[i] == wave[i + 1]:
                i += 1
                c += 1
                if i >= (len(wave) - 1):
                    break
            sequences.append(c)
        x = sum(sequences) / len(sequences)
        if x < 2.5:
            bits.append("2")
            continue
        if x > 6.0:
            bits.append("0")
            continue
        bits.append("1")

    for char in grouper(bits, 8):
        print(chr(int("".join(char[1:6]), 3)), end="")

    print()


solve(actual_input)
