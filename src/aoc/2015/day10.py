from itertools import groupby

from aoc_utils import get_input_data

actual_input = get_input_data(2015, 10)


def solve(inputs):
    def look_and_say(digits):
        return "".join(str(len(list(l))) + d for d, l in groupby(digits))

    digits = inputs
    for _ in range(40):
        digits = look_and_say(digits)
    print(f"Part 1: {len(digits)}")

    for _ in range(10):
        digits = look_and_say(digits)
    print(f"Part 2: {len(digits)}\n")


solve(actual_input)
