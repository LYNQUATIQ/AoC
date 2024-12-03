"""https://adventofcode.com/2024/day/3"""

from aoc_utils import get_input_data
import re

actual_input = get_input_data(2024, 3)


sample_input = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
)


def solve(inputs: str):
    part1, part2 = 0, 0
    mul_enabled = True
    while inputs:
        if m := re.match(r"^mul\(\d{1,3},\d{1,3}\)", inputs):
            a, b = map(int, m.group().strip("mul()").split(","))
            part1 += a * b
            if mul_enabled:
                part2 += a * b
            inputs = inputs[len(m.group()) :]
            continue
        if inputs.startswith("do()"):
            mul_enabled = True
            inputs = inputs[4:]
            continue
        if inputs.startswith("don't()"):
            mul_enabled = False
            inputs = inputs[7:]
            continue
        inputs = inputs[1:]

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
