"""https://adventofcode.com/2023/day/19"""
from __future__ import annotations

import math
import os
import re

from collections import defaultdict
from dataclasses import dataclass

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


REJECTED, ACCEPTED = "R", "A"
START = "in"

MIN, MAX = 0, 1

EVERYWHERE = ((1, 4000), (1, 4000), (1, 4000), (1, 4000))


Rules = list[tuple[tuple[int, str, int] | None, str]]
Workflows = dict[str, Rules]
Part = tuple[int, int, int, int]
Range = tuple[int, int]


def is_accepted(part: Part, workflow_tests: Workflows) -> bool:
    workflow = START
    while workflow not in (REJECTED, ACCEPTED):
        for test, next_workflow in workflow_tests[workflow]:
            if test is None:
                break
            i, op, value = test
            if (op == "<" and part[i] < value) or (op == ">" and part[i] > value):
                break
        workflow = next_workflow
    return workflow == ACCEPTED


@dataclass(frozen=True)
class RatingsSpace:
    """Dataclass for a 4D space representing ranges of ratings"""

    space: tuple[Range, Range, Range, Range]

    @property
    def combinations(self):
        """The number of combinations within this space."""
        return math.prod(r[MAX] + 1 - r[MIN] for r in self.space)

    def intersect(self, other: RatingsSpace) -> RatingsSpace | None:
        return RatingsSpace(
            tuple(
                (
                    max(self.space[i][MIN], other.space[i][MIN]),
                    min(self.space[i][MAX], other.space[i][MAX]),
                )
                for i in range(4)
            )
        )

    def union(self, other: RatingsSpace) -> set[RatingsSpace]:
        """The set of *disjoint* spaces representing the union of this space and other"""
        disjoint_spaces = set(self)
        this_space = list(self.space)
        for i in range(4):
            if other.space[i][MIN] < this_space[i][MIN]:
                new_space = this_space
                new_space[i] = (other.space[i][MIN], this_space[i][MIN] - 1)
                disjoint_spaces.add(RatingsSpace(new_space))
            if other.space[i][MAX] > this_space[i][MAX]:
                new_space = this_space
                new_space[i] = (this_space[i][MAX] + 1, other.space[i][MAX])
                disjoint_spaces.add(RatingsSpace(new_space))
            this_space[i] = max(this_space[i][MIN], other.space[i][MIN]), min(
                this_space[i][MAX], other.space[i][MAX]
            )
        return disjoint_spaces


def solve(inputs: str):
    workflow_data, parts_data = (data.splitlines() for data in inputs.split("\n\n"))

    workflow_tests = {}
    for label, test_data in (w[:-1].split("{") for w in workflow_data):
        tests = []
        for test_input in test_data.split(","):
            if (match := re.match(r"([(xmas])([<>])(\d+):(\w+)", test_input)) is None:
                tests.append((None, test_input))
            else:
                category, op, value, destination = match.groups()
                tests.append((("xmas".index(category), op, int(value)), destination))
        workflow_tests[label] = tests

    parts = [tuple(int(n) for n in re.findall(r"\d+", p)) for p in parts_data]
    total = sum(sum(part) for part in parts if is_accepted(part, workflow_tests))
    print(f"Part 1: {total}")

    ratings_to_get_to: dict[set[RatingsSpace]] = defaultdict(set[RatingsSpace])
    ratings_to_get_to[START].add(RatingsSpace(EVERYWHERE))
    to_visit = {START}
    while to_visit:
        here = to_visit.pop()
        tests = workflow_tests.get(here, [])
        for ratings_to_here in ratings_to_get_to[here]:
            ratings_to_next = RatingsSpace(ratings_to_here.space)
            for test, destination in tests:
                to_visit.add(destination)
                if test is None:
                    ratings_to_get_to[destination].add(ratings_to_next)
                    continue
                i, op, v = test
                pass_ratings, fail_ratings = list(EVERYWHERE), list(EVERYWHERE)
                ratings_i = (
                    (v + 1 if op == ">" else 1),
                    (v - 1 if op == "<" else 4000),
                )
                pass_ratings[i] = ratings_i
                fail_ratings_i = ((v if op == "<" else 1), (v if op == ">" else 4000))
                fail_ratings[i] = fail_ratings_i

                dest_ratings = ratings_to_next.intersect(RatingsSpace(pass_ratings))
                if dest_ratings is not None:
                    ratings_to_get_to[destination].add(dest_ratings)
                ratings_to_next = ratings_to_next.intersect(RatingsSpace(fail_ratings))
                if ratings_to_next is None:
                    break

    print(f"Part 2: {sum(r.combinations for r in ratings_to_get_to[ACCEPTED])}\n")


solve(sample_input)
solve(actual_input)
