"""https://adventofcode.com/2024/day/2"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 2)
sample_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def test_report(report: list[int]) -> bool:
    all_increasing = all(a > b for a, b in zip(report[:-1], report[1:]))
    all_decreasing = all(a < b for a, b in zip(report[:-1], report[1:]))
    in_range = all(1 <= abs(a - b) <= 3 for a, b in zip(report[:-1], report[1:]))
    return (all_increasing or all_decreasing) and in_range


def solve(inputs: str):
    reports = [list(map(int, line.split())) for line in inputs.splitlines()]

    safe = 0
    for report in reports:
        safe += test_report(report)
    print(f"Part 1: {safe}")

    safe = 0
    for report in reports:
        is_safe = test_report(report)
        if not is_safe:
            for i in range(len(report)):
                is_safe = test_report(report[:i] + report[i + 1 :])
                if is_safe:
                    break
        if is_safe:
            safe += is_safe
    print(f"Part 2: {safe}\n")


solve(sample_input)
solve(actual_input)
