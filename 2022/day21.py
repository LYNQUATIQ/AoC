"""https://adventofcode.com/2022/day/21"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day21_input.txt")) as f:
    actual_input = f.read()


sample_input = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

from collections import defaultdict


def solve(inputs: str) -> None:
    operations = {}
    values = {}
    used_humn = {"humn"}
    target, to_solve = 0, "xxxx"
    for monkey, token in map(lambda x: x.split(": "), inputs.splitlines()):
        if any(op in token for op in "+-/*"):
            a, operation, b = token.split()
            operations[monkey] = (a, operation, b, False)
        else:
            values[monkey] = int(token)

    while not "root" in values:
        for monkey, (a, operation, b, solved) in operations.items():
            if solved:
                continue
            if a in values and b in values:
                result = {
                    "+": values[a] + values[b],
                    "-": values[a] - values[b],
                    "*": values[a] * values[b],
                    "/": values[a] // values[b],
                }[operation]
                values[monkey] = result
                operations[monkey] = (a, operation, b, True)
                operations[monkey] = (a, operation, b, True)
                if a in used_humn or b in used_humn:
                    used_humn.add(monkey)
                if monkey == "root":
                    assert (a in used_humn) != (b in used_humn)
                    if a in used_humn:
                        target, to_solve = values[b], a
                    else:
                        target, to_solve = values[a], b

    print(f"Part 1: {values['root']}")

    while to_solve != "humn":
        a, operation, b, _ = operations[to_solve]
        assert (a in used_humn) != (b in used_humn)
        if a in used_humn:
            to_solve = a
            target = {
                "+": target - values[b],
                "-": target + values[b],
                "*": target // values[b],
                "/": target * values[b],
            }[operation]
        else:
            to_solve = b
            target = {
                "+": target - values[a],
                "-": values[a] - target,
                "*": target // values[a],
                "/": values[a] // target,
            }[operation]

    print(f"Part 2: {target}\n")


solve(sample_input)
solve(actual_input)
