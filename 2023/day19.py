"""https://adventofcode.com/2023/day/19"""
import os
import re


with open(os.path.join(os.path.dirname(__file__), "inputs/day19_input.txt")) as f:
    actual_input = f.read()


sample_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

COOL = "x"
MUSICAL = "m"
AERODYNAMIC = "a"
SHINY = "s"

REJECTED, ACCEPTED = "R", "A"
START = "in"

OPERATORS = {">": lambda a, b: a > b, "<": lambda a, b: a < b}


def is_accepted(part, workflows) -> bool:
    workflow = START
    while workflow not in (REJECTED, ACCEPTED):
        tests = workflows[workflow]
        for test, next_workflow in tests:
            if test is None:
                break
            category, operator, value = test
            if operator(part[category], value):
                break
        workflow = next_workflow
    return workflow == ACCEPTED


def solve(inputs: str):
    workflows_input, parts_input = inputs.split("\n\n")

    workflows = {}
    for line in workflows_input.splitlines():
        label, test_inputs = line[:-1].split("{")
        tests = []
        for test_input in test_inputs.split(","):
            if ":" not in test_input:
                tests.append((None, test_input))
            else:
                test, destination = test_input.split(":")
                category, comparison, value = test[0], test[1], int(test[2:])
                tests.append(((category, OPERATORS[comparison], value), destination))
        workflows[label] = tests

    parts = []
    for line in parts_input.splitlines():
        values = [int(n) for n in re.findall(r"\d+", line)]
        categories = re.findall(r"(\w)=", line)
        parts.append(dict(zip(categories, values)))

    total = sum(sum(part.values()) for part in parts if is_accepted(part, workflows))
    print(f"Part 1: {total}")

    # state = START
    # to_visit = {START}
    # while to_visit:
    #     workflow = to_visit.pop()

    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)

"""
Each of the four ratings (x, m, a, s) can have an integer value ranging from a 
minimum of 1 to a maximum of 4000. Of all possible distinct combinations of ratings, 
your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that 
will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted 
you to sort is no longer relevant. 
How many distinct combinations of ratings will be accepted by the Elves' workflows?
"""
