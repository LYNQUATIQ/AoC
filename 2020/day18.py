import math
import os
import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

BRACKET= re.compile(r"^(?P<left>[\d+*()]*)\((?P<brackets>[\d+*]+)\)(?P<right>[\d+*()]*)$")
STAR= re.compile(r"^(?P<left>[\d*+]+)(?P<oper>\*)(?P<right>[\d+]+)$")
PLUS= re.compile(r"^(?P<left>[\d*+]+)(?P<oper>\+)(?P<right>[\d*]+)$")
ANY= re.compile(r"^(?P<left>[\d*+]+)(?P<oper>[*+])(?P<right>\d+)$")


def evaluate_expression(expression, regexes):
    matches = (regex.match(expression) for regex in regexes)
    try:
        match = next(m for m in matches if m is not None)
    except StopIteration:
        return expression

    if "brackets" in match.groupdict():
        contents = evaluate_expression(match.group('brackets'), regexes)
        expression = match['left'] + str(contents) + match['right'] 
        return evaluate_expression(expression, regexes)

    a = evaluate_expression(match.group('left'), regexes)
    b = evaluate_expression(match.group('right'), regexes)
    return { "*": math.prod, "+": sum }[match['oper']]((int(a), int(b)))


def solve(inputs):
    part1, part2 = 0, 0
    for expression in[line.replace(" ","") for line in inputs.splitlines()]:
        part1 += evaluate_expression(expression, [BRACKET, ANY])
        part2 += evaluate_expression(expression, [BRACKET, STAR, PLUS])

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
