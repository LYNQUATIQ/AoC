"""https://adventofcode.com/2023/day/12"""

import os

from functools import cache


with open(os.path.join(os.path.dirname(__file__), "inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


@cache
def parse_spring_record(record: str, ranges: tuple[int, ...]) -> int:
    # If we've run out of ranges return 0 if we still have broken springs
    if not ranges:
        return int("#" not in record)

    # If we still have springs left but have consumed too much of the record return 0
    if sum(ranges) + len(ranges) - 1 > len(record):
        return 0

    # Find all the possible positions for the first range and then recurse the remainder
    record = "." + record + "."
    retval = 0
    for i, symbol in enumerate(record[: -(ranges[0] + 2)]):
        if symbol == "#":
            break
        if (
            symbol in ".?"
            and record[i + 1 : i + ranges[0] + 1].replace("?", "#") == "#" * ranges[0]
            and record[i + ranges[0] + 1] in ".?"
        ):
            retval += parse_spring_record(record[i + ranges[0] + 2 :], ranges[1:])
    return retval


def solve(inputs: str):
    record_values = [line.split(" ") for line in inputs.splitlines()]

    options = sum(
        parse_spring_record(record, tuple(int(n) for n in values.split(",")))
        for record, values in record_values
    )
    print(f"Part 1: {options}")

    options = sum(
        parse_spring_record(
            "?".join([record] * 5), tuple([int(n) for n in values.split(",")] * 5)
        )
        for record, values in record_values
    )
    print(f"Part 2: {options}\n")


solve(sample_input)
solve(actual_input)
