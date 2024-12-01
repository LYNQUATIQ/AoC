"""https://adventofcode.com/2021/day/10"""

import os
from functools import reduce
from statistics import median

with open(os.path.join(os.path.dirname(__file__), "inputs/day10_input.txt")) as f:
    actual_input = f.read()

sample_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


CLOSING = {")": "(", "]": "[", "}": "{", ">": "<"}
POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137, "(": 1, "[": 2, "{": 3, "<": 4}


def solve(inputs):
    part1, part2 = 0, []
    for line in inputs.splitlines():
        openings, incorrect = [], False
        for bracket in line:
            if bracket in CLOSING:
                if CLOSING[bracket] != openings.pop():
                    incorrect = True
                    break
            else:
                openings.append(bracket)
        if incorrect:
            part1 += POINTS[bracket]
        else:
            part2.append(reduce(lambda a, b: a * 5 + POINTS[b], openings[::-1], 0))

    print(f"Part 1: {part1}")
    print(f"Part 2: {median(part2)}\n")


solve(sample_input)
solve(actual_input)
