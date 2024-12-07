"""https://adventofcode.com/2024/day/7"""

import re

from aoc_utils import get_input_data, print_time_taken

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

TWO_OPERATIONS = (lambda a, b: a + b, lambda a, b: a * b)
THREE_OPERATIONS = (lambda a, b: a + b, lambda a, b: a * b, lambda a, b: int(f"{a}{b}"))


def compute_test_values(values: list[int], target: int, operations) -> list[int]:
    lhs_values, rhs = values[:-1], values[-1]
    if not lhs_values:
        if rhs > target:
            return []
        return [rhs]

    lhs_test_values = compute_test_values(lhs_values, target, operations)
    return [operation(lhs, rhs) for operation in operations for lhs in lhs_test_values]


def total_calibrations(equations, operations_list) -> int:
    total_calibration = 0
    for target, values in equations:
        if target in compute_test_values(values, target, operations_list):
            total_calibration += target
    return total_calibration


@print_time_taken
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
