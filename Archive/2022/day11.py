"""https://adventofcode.com/2022/day/11"""

from __future__ import annotations
import os
import math
import re

from dataclasses import dataclass
from functools import partial
from typing import Callable


with open(os.path.join(os.path.dirname(__file__), "inputs/day11_input.txt")) as f:
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


def multiply_item(value: int, multiplier: int) -> int:
    return value * multiplier


def add_to_item(value: int, adjustment: int) -> int:
    return value + adjustment


def square_item(value: int) -> int:
    return value**2


@dataclass
class Monkey:
    items: list[int]
    inspection: Callable[[int], int]
    divisibility_test: int
    if_true: int
    if_false: int
    inspections: int = 0


def do_monkey_business(inputs: str, rounds: int, reduce_worry: bool) -> int:
    monkeys: list[Monkey] = []
    for attributes in map(str.splitlines, inputs.split("\n\n")):
        items = list(map(int, re.findall(r"\d+", attributes[1])))
        match attributes[2].split()[-2:]:
            case ["*", "old"]:
                inspection = square_item
            case ["*", value]:
                inspection = partial(multiply_item, multiplier=int(value))
            case ["+", value]:
                inspection = partial(add_to_item, adjustment=int(value))
        divisibility_test = int(attributes[3].split()[-1])
        if_true = int(attributes[4].split()[-1])
        if_false = int(attributes[5].split()[-1])
        monkeys.append(Monkey(items, inspection, divisibility_test, if_true, if_false))

    modulo = math.prod(m.divisibility_test for m in monkeys)
    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items:
                monkey.inspections += 1
                item = monkey.inspection(item) % modulo
                if reduce_worry:
                    item //= 3
                if item % monkey.divisibility_test == 0:
                    monkeys[monkey.if_true].items.append(item)
                else:
                    monkeys[monkey.if_false].items.append(item)
            monkey.items = []

    return math.prod(sorted(m.inspections for m in monkeys)[-2:])


def solve(inputs: str) -> None:
    print(f"Part 1: {do_monkey_business(inputs, 20, reduce_worry=True)}")
    print(f"Part 2: {do_monkey_business(inputs, 10_000, reduce_worry=False)}\n")


solve(sample_input)
solve(actual_input)
