import math
import os
import re

with open(os.path.join(os.path.dirname(__file__), f"inputs/day18_input.txt")) as f:
    actual_input = f.read()

sample_input = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

BRACKET = re.compile(r"^(?P<left>.*)\((?P<brackets>[\d+*]+)\)(?P<right>.*)$")
STAR = re.compile(r"^(?P<left>[\d*+]+)(?P<operator>\*)(?P<right>[\d+]+)$")
PLUS = re.compile(r"^(?P<left>[\d*+]+)(?P<operator>\+)(?P<right>[\d*]+)$")
ANY = re.compile(r"^(?P<left>[\d*+]+)(?P<operator>[*+])(?P<right>\d+)$")


def evaluate(expression, regexes):
    try:
        match = next(m for m in (r.match(expression) for r in regexes) if m is not None)
    except StopIteration:
        return expression

    if "brackets" in match.groupdict():
        contents = evaluate(match.group("brackets"), regexes)
        return evaluate(match["left"] + str(contents) + match["right"], regexes)

    a = int(evaluate(match.group("left"), regexes))
    b = int(evaluate(match.group("right"), regexes))
    return {"*": math.prod, "+": sum}[match["operator"]]((a, b))


def solve(inputs):
    part1, part2 = 0, 0
    for expression in (line.replace(" ", "") for line in inputs.splitlines()):
        part1 += evaluate(expression, [BRACKET, ANY])
        part2 += evaluate(expression, [BRACKET, STAR, PLUS])

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
