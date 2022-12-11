"""https://adventofcode.com/2022/day/11"""
from __future__ import annotations
import os
import math
import re

from dataclasses import dataclass
from functools import partial
from typing import Callable, Type


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

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)
MODULAR_INVERSE_3 = {2: 1, 5: 2, 7: 5, 11: 4, 13: 9, 17: 6, 19: 13, 23: 8}


class Item:
    def __init__(self, value: int) -> None:
        self.value = value
        self.remainders = {p: value % p for p in PRIMES}

    def divisible_by(self, prime: int) -> bool:
        return self.value % prime == 0

    def divide_by_3(self) -> None:
        self.value = self.value // 3

    @staticmethod
    def multiply_item(item: Item, multiplier: int) -> None:
        item.value *= multiplier

    @staticmethod
    def add_to_item(item: Item, adjustment: int) -> None:
        item.value += adjustment

    @staticmethod
    def square_item(item: Item) -> None:
        item.value **= 2


class ModuloItem(Item):
    def __init__(self, value: int) -> None:
        self.remainders = {p: value % p for p in PRIMES}

    def divisible_by(self, prime: int) -> bool:
        return self.remainders[prime] == 0

    def divide_by_3(self) -> None:
        raise NotImplementedError
        # self.add_to_item(self, 3 - self.remainders[3])
        # for p, r in self.remainders.items():
        #     self.remainders[p] = 0 if p == 3 else (r * MODULAR_INVERSE_3[p]) % p

    @staticmethod
    def multiply_item(item: Item, multiplier: int) -> None:
        for p, r in item.remainders.items():
            item.remainders[p] = (r * multiplier) % p

    @staticmethod
    def add_to_item(item: Item, adjustment: int) -> None:
        for p, r in item.remainders.items():
            item.remainders[p] = (r + adjustment) % p

    @staticmethod
    def square_item(item: Item) -> None:
        for p, r in item.remainders.items():
            item.remainders[p] = (r ** 2) % p


@dataclass
class Monkey:
    items: list[Item | ModuloItem]
    inspect: Callable[[Item], None]
    divisibility_test: int
    if_true: int
    if_false: int
    inspections: int = 0


def parse_monkeys(inputs: str, item_cls: Type) -> list[Monkey]:
    monkeys: list[Monkey] = []
    for attributes in map(str.splitlines, inputs.split("\n\n")):
        items = [item_cls(x) for x in map(int, re.findall(r"\d+", attributes[1]))]
        operator, value = attributes[2].split()[-2:]
        inspect = item_cls.square_item
        if value != "old":
            if operator == "*":
                inspect = partial(item_cls.multiply_item, multiplier=int(value))
            else:
                inspect = partial(item_cls.add_to_item, adjustment=int(value))
        divisibility_test = int(attributes[3].split()[-1])
        if_true = int(attributes[4].split()[-1])
        if_false = int(attributes[5].split()[-1])
        monkeys.append(Monkey(items, inspect, divisibility_test, if_true, if_false))
    return monkeys


def do_monkey_business(inputs: str, rounds: int, reduce_worry: bool) -> int:
    monkeys = parse_monkeys(inputs, Item if reduce_worry else ModuloItem)

    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items:
                monkey.inspections += 1
                monkey.inspect(item)
                if reduce_worry:
                    item.divide_by_3()
                if item.divisible_by(monkey.divisibility_test):
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
