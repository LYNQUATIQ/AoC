"""https://adventofcode.com/2023/day/12"""
import os

from collections import Counter
from itertools import chain, combinations


with open(os.path.join(os.path.dirname(__file__), "inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

POSSIBILITIES = {1: (".#.", ".?.", "")}


def possibilities(arrangement: str, values: tuple[int, ...]) -> int:
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
        arrangement, values_string = line.split(" ")
        values = tuple(int(n) for n in values_string.split(","))
        options += possibilities(arrangement, values)
    print(f"Part 1: {options}")

    # options = 0
    # for line in inputs.splitlines():
    #     arrangement, values_string = line.split(" ")
    #     values = [int(n) for n in values_string.split(",")] * 5
    #     options += possibilities(arrangement * 5, values)
    # print(f"Part 2: {options}\n")


solve(sample_input)
solve(actual_input)
