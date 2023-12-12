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
def parse_condition_record(condition_record: str, groups: tuple[int, ...]) -> int:
    # If run out of groups return 0 (infeasible) if we still have damaged springs, or 1
    # if we can assume the remaining arranagment is all operational
    if not groups:
        return int("#" not in condition_record)

    # If we still have groups left but have consumed too much of the record return 0
    if sum(groups) + len(groups) - 1 > len(condition_record):
        return 0

    # Find all the legitimate positions for the first group
    condition_record = "." + condition_record + "."
    group, groups = groups[0], groups[1:]
    i, retval = 0, 0
    for i, symbol in enumerate(condition_record[: -(group + 2)]):
        if symbol == "#":
            break
        target_group = condition_record[i + 1 : i + group + 1].replace("?", "#")
        if (
            symbol in ".?"
            and target_group == "#" * group
            and condition_record[i + group + 1] in ".?"
        ):
            retval += parse_condition_record(condition_record[i + group + 2 :], groups)
        i += 1
    return retval


def solve(inputs):
    options = 0
    for line in inputs.splitlines():
        condition_record, values_string = line.split(" ")
        values = tuple(int(n) for n in values_string.split(","))
        options += parse_condition_record(condition_record, values)
    print(f"Part 1: {options}")

    options = 0
    for line in inputs.splitlines():
        condition_record, values_string = line.split(" ")
        condition_record = "?".join(r for r in [condition_record] * 5)
        values = tuple([int(n) for n in values_string.split(",")] * 5)
        options += parse_condition_record(condition_record, values)
    print(f"Part 2: {options}\n")


solve(sample_input)
solve(actual_input)
