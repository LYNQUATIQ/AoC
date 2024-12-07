"""https://adventofcode.com/2024/day/7"""

import re
from itertools import product

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 7)
example_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

TWO_OPERATIONS = [lambda a, b: a + b, lambda a, b: a * b]
THREE_OPERATIONS = [lambda a, b: a + b, lambda a, b: a * b, lambda a, b: int(f"{a}{b}")]


def total_calibrations(equations, operations_list) -> int:
    total_calibration = 0
    for target, values in equations:
        for operators in product(operations_list, repeat=len(values) - 1):
            equation_sum = values[0]
            for operation, value in zip(operators, values[1:]):
                equation_sum = operation(equation_sum, value)
            if equation_sum == target:
                total_calibration += target
                break
    return total_calibration


def solve(inputs: str):
    equations = [
        (target, values)
        for target, *values in (
            map(int, re.findall(r"-?\d+", line)) for line in inputs.splitlines()
        )
    ]
    print(f"Part 1: {total_calibrations(equations, TWO_OPERATIONS)}")
    print(f"Part 2: {total_calibrations(equations, THREE_OPERATIONS)}\n")


solve(example_input)
solve(actual_input)
