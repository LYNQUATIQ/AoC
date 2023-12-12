"""https://adventofcode.com/2023/day/12"""
import os

from collections import Counter
from itertools import combinations
import re


with open(os.path.join(os.path.dirname(__file__), "inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def parse_condition_record(
    condition_record: str, groups: tuple[int, ...], debug=False, spacer=""
) -> int:
    spacer += "  "
    # If run out of groups return 0 (infeasible) if we still have damaged springs, or 1
    # if we can assume the remaining arranagment is all operational
    if not groups:
        return int("#" not in condition_record)

    condition_record = condition_record.lstrip(".")

    # If we still have groups left but have consumed too much of the record return 0
    if sum(groups) + len(groups) - 1 > len(condition_record):
        return 0

    # Find all the legitimate positions for the first group
    condition_record = "." + condition_record + "."
    group, groups = groups[0], groups[1:]
    i = 0
    retval = 0
    for i, symbol in enumerate(condition_record):
        if symbol == "#":
            break
        if match := re.match(rf"^[\.\?][\?\#]{{{group}}}[\.\?]", condition_record[i:]):
            n = parse_condition_record(
                condition_record[i + match.end() :],
                groups,
                debug=debug,
                spacer=spacer,
            )
            if debug:
                print(
                    spacer,
                    condition_record[i + match.end() :],
                    groups,
                    " <- ",
                    n,
                )
            retval += n
        i += 1
    return retval


def correct_parse(arrangement: str, values: tuple[int, ...]) -> int:
    valid = 0
    missing = sum(values) - Counter(arrangement)["#"]
    question_marks = {i for i, c in enumerate(arrangement) if c == "?"}
    for sublist in combinations(question_marks, missing):
        option = ""
        for i, c in enumerate(arrangement):
            if i in question_marks:
                option += "#" if i in sublist else "."
            else:
                option += c
        valid += tuple(len(t) for t in option.split(".") if t != "") == values
    return valid


def solve(inputs):
    options = 0
    for line in inputs.splitlines():
        condition_record, values_string = line.split(" ")
        values = tuple(int(n) for n in values_string.split(","))

        p = parse_condition_record(condition_record, values)
        # p_correct = correct_parse(condition_record, values)
        # if p != p_correct:
        #     print(f"{line}  <-  WRONG: {p}    CORRECT: {p_correct}")
        #     parse_condition_record(condition_record, values, debug=True)
        #     break
        options += p

    print(f"Part 1: {options}")

    # options = 0
    # for line in inputs.splitlines():
    #     condition_record, values_string = line.split(" ")
    #     values = [int(n) for n in values_string.split(",")] * 5
    #     options += possibilities(condition_record * 5, values)
    print(f"Part 2: {options}\n")


solve(sample_input)
solve(actual_input)
# line = """?????.??##?????????. 2,6,2"""
# condition_record, values_string = line.split(" ")
# tokens = deque([t for t in re.sub(r"\.+", ".", condition_record).split(".") if t != ""])
# values = deque(int(n) for n in values_string.split(","))
# possibilities(tokens, values)
