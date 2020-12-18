import os
import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))"""


RE_EXPRESSION = re.compile(r"^(?P<left>[\d+*()]*)\((?P<expression>[\d+*]+)\)(?P<right>[\d+*()]*)$")
RE_OPERATOR = re.compile(r"^(?P<left>[\d*+]+)(?P<operator>[+*])(?P<value>\d+)$")
RE_MULTIPLY = re.compile(r"^(?P<left>[\d*+]+)(?P<operator>[*])(?P<right>[\d+]+)$")

def evaluate_sum_pt2(expression):
    match = RE_MULTIPLY.match(expression)
    if match is None:
        return evaluate_sum_pt1(expression)
    left = evaluate_sum_pt2(match.group('left'))
    right = evaluate_sum_pt2(match.group('right'))
    return left * right

def evaluate_sum_pt1(expression):
    match = RE_OPERATOR.match(expression)
    if match is None:
        return int(expression)
    value = int(match.group('value'))
    left = evaluate_sum_pt1(match.group('left'))
    if match.group('operator') == "+":
        return left + value
    return left * value

def evaluate_expression(expression, evaluate_fn):
    match = RE_EXPRESSION.match(expression)
    if match is None:
        return evaluate_fn(expression)
    bracketed_expression = str(evaluate_fn(match.group('expression')))
    expression = match.group('left') + bracketed_expression + match.group('right')
    return evaluate_expression(expression,evaluate_fn)


def solve(inputs):
    part1, part2 = 0, 0
    for expression in[line.replace(" ","") for line in inputs.splitlines()]:
        part1 += evaluate_expression(expression, evaluate_sum_pt1)
        part2 += evaluate_expression(expression, evaluate_sum_pt2)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
