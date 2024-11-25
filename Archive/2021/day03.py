"""https://adventofcode.com/2021/day/3"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day03_input.txt")) as f:
    actual_input = f.read()

sample_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def solve(inputs):
    values = inputs.splitlines()
    bit_count = len(values[0])

    gamma_bits = tuple(column.count("1") > column.count("0") for column in zip(*values))
    gamma = sum(2**i for i, c in enumerate(reversed(gamma_bits)) if c)
    epsilon = gamma ^ (2**bit_count - 1)
    print(f"Part 1: {gamma * epsilon}")

    def get_rating(doing_o2: bool):
        rating_values = values
        for i in range(bit_count):
            ones: list[str] = []
            zeroes: list[str] = []
            for value in rating_values:
                (ones if value[i] == "1" else zeroes).append(value)
            more_ones = len(ones) >= len(zeroes)
            if doing_o2:
                rating_values = ones if more_ones else zeroes
            else:
                rating_values = zeroes if more_ones else ones
            if len(rating_values) == 1:
                break
        return int(rating_values.pop(), 2)

    print(f"Part 2: {get_rating(True) * get_rating(False)}\n")


solve(sample_input)
solve(actual_input)
