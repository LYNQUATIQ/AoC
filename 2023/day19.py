"""https://adventofcode.com/2023/day/19"""
import math
import os
import re
from collections import defaultdict
from typing import Sequence

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


REJECTED, ACCEPTED, START = "R", "A", "in"
ALL_COMBINATIONS = ((1, 4000), (1, 4000), (1, 4000), (1, 4000))

Workflows = dict[str, Sequence[tuple[tuple[int, str, int] | None, str]]]
Combo = Sequence[tuple[int, int]]


def part_accepted(part: Sequence[int], workflow_rules: Workflows) -> bool:
    workflow = START
    while workflow not in (REJECTED, ACCEPTED):
        for rule, next_workflow in workflow_rules[workflow]:
            if rule is None:
                break
            category, gt_lt, bound = rule
            if {"<": part[category] < bound, ">": part[category] > bound}[gt_lt]:
                break
        workflow = next_workflow
    return workflow == ACCEPTED


def combo_volume(combo: Combo) -> int:
    return math.prod(max_bound + 1 - min_bound for min_bound, max_bound in combo)


def combo_intersect(this: Combo, other: Combo) -> Combo:
    return tuple(
        (max(min_this, min_other), min(max_this, max_other))
        for (min_this, max_this), (min_other, max_other) in zip(this, other)
    )


def solve(inputs: str):
    workflows_data, parts_data = (data.splitlines() for data in inputs.split("\n\n"))

    workflow_rules = {}
    for label, rules_data in (w[:-1].split("{") for w in workflows_data):
        rules = []
        for rule_input in rules_data.split(","):
            if match := re.match(r"([(xmas])([<>])(\d+):(\w+)", rule_input):
                category, gt_lt, bound, destination = match.groups()
                rules.append((("xmas".index(category), gt_lt, int(bound)), destination))
            else:
                rules.append((None, rule_input))
        workflow_rules[label] = rules

    parts = [tuple(int(n) for n in re.findall(r"\d+", p)) for p in parts_data]
    total = sum(sum(part) for part in parts if part_accepted(part, workflow_rules))
    print(f"Part 1: {total}")

    combos_to = defaultdict(set[Combo], {START: {ALL_COMBINATIONS}})
    to_visit = {START}
    while to_visit:
        this_workflow = to_visit.pop()
        rules = workflow_rules.get(this_workflow, [])
        for combo_here in combos_to[this_workflow]:
            for rule, next_workflow in rules:
                to_visit.add(next_workflow)
                if rule is None:
                    combos_to[next_workflow].add(combo_here)
                    continue
                category, gt_lt, x = rule
                pass_combo, fail_combo = list(ALL_COMBINATIONS), list(ALL_COMBINATIONS)
                pass_combo[category] = tuple(
                    (x + 1 if gt_lt == ">" else 1), (x - 1 if gt_lt == "<" else 4000)
                )
                fail_combo[category] = tuple(
                    (x if gt_lt == "<" else 1), (x if gt_lt == ">" else 4000)
                )
                next_combo = combo_intersect(combo_here, pass_combo)
                if next_combo is not None:
                    combos_to[next_workflow].add(next_combo)
                combo_here = combo_intersect(combo_here, fail_combo)
                if combo_here is None:
                    break

    print(f"Part 2: {sum(combo_volume(r) for r in combos_to[ACCEPTED])}\n")


solve(sample_input)
solve(actual_input)
