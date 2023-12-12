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
    # If we've run out of groups return 0 (infeasible) if we still have damaged springs
    # (or 1 if we can assume the remaining arranagment is all operational)
    if not groups:
        return int("#" not in condition_record)

    # If we still have groups left but have consumed too much of the record return 0
    if sum(groups) + len(groups) - 1 > len(condition_record):
        return 0

    # Find all the legitimate start positions of first group and recurse the remainder
    group, groups = groups[0], groups[1:]
    condition_record = "." + condition_record + "."
    i, retval = 0, 0
    for i, symbol in enumerate(condition_record[: -(group + 2)]):
        if symbol == "#":
            break
        if (
            symbol in ".?"
            and condition_record[i + 1 : i + group + 1].replace("?", "#") == "#" * group
            and condition_record[i + group + 1] in ".?"
        ):
            retval += parse_condition_record(condition_record[i + group + 2 :], groups)
        i += 1
    return retval


def solve(inputs):
    condition_records = [line.split(" ") for line in inputs.splitlines()]

    options = sum(
        parse_condition_record(
            condition_record, tuple(int(n) for n in values.split(","))
        )
        for condition_record, values in condition_records
    )
    print(f"Part 1: {options}")

    options = sum(
        parse_condition_record(
            "?".join(r for r in [condition_record] * 5),
            tuple([int(n) for n in values.split(",")] * 5),
        )
        for condition_record, values in condition_records
    )
    print(f"Part 2: {options}\n")


solve(sample_input)
solve(actual_input)
