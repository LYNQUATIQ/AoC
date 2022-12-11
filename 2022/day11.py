"""https://adventofcode.com/2022/day/11"""
import os
import math
import re

from dataclasses import dataclass
from typing import Callable

with open(os.path.join(os.path.dirname(__file__), f"inputs/day11_input.txt")) as f:
    actual_input = f.read()


sample_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


@dataclass
class Monkey:
    monkey: int
    items: list[int]
    operation: Callable
    adjustment: int
    divisibility: int
    if_true: int
    if_false: int
    inspections: int = 0


addition = lambda a, b: a + b
multiplication = lambda a, b: a * b


def solve(inputs: str) -> None:
    monkeys: list[Monkey] = []
    for data in inputs.split("\n\n"):
        lines = data.splitlines()
        monkey = int(lines[0][7:-1])
        items = list(map(int, re.findall(r"\d+", lines[1])))
        tokens = lines[2].split()
        operation = multiplication if tokens[-2] == "*" else addition
        adjustment = -999 if tokens[-1] == "old" else int(tokens[-1])
        divisibility = int(lines[3].split()[-1])
        if_true = int(lines[4].split()[-1])
        if_false = int(lines[5].split()[-1])
        monkeys.append(
            Monkey(
                monkey, items, operation, adjustment, divisibility, if_true, if_false
            )
        )

    round = 1
    while True:
        for m in monkeys:
            for worry_level in m.items:
                adjustment = worry_level if m.adjustment < 0 else m.adjustment
                worry_level = m.operation(worry_level, adjustment)
                worry_level = worry_level // 3
                if worry_level % m.divisibility == 0:
                    monkeys[m.if_true].items.append(worry_level)
                else:
                    monkeys[m.if_false].items.append(worry_level)
            m.inspections += len(m.items)
            m.items = []

        # print("After round ", round)
        # for m in monkeys:
        #     print(f'Monkey {m.monkey}: {", ".join(map(str,m.items))}')
        # print()

        if round == 20:
            monkey_business = math.prod(sorted(m.inspections for m in monkeys)[-2:])
            break
        round += 1

    print(f"Part 1: {monkey_business}")
    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
