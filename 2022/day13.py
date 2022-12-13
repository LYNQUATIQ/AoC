"""https://adventofcode.com/2022/day/13"""
from __future__ import annotations

import json
import math
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day13_input.txt")) as f:
    actual_input = f.read()


sample_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


class PacketData(str):
    def __lt__(self, other: object) -> bool:
        assert isinstance(other, PacketData)

        if self == "[]" or other == "[]":
            return self == "[]"
        l_items, r_items = json.loads(self), json.loads(other)
        left, right = PacketData(l_items[0]), PacketData(r_items[0])
        if left == right:
            return PacketData(l_items[1:]) < PacketData(r_items[1:])
        if left.isdigit() and right.isdigit():
            return int(left) < int(right)
        if left.isdigit():
            return PacketData(f"[[{left}],{l_items[1:]}]") < other
        if right.isdigit():
            return self < PacketData(f"[[{right}],{r_items[1:]}]")
        return left < right


DIVIDERS = [PacketData("[[2]]"), PacketData("[[6]]")]


def solve(inputs: str) -> None:
    pairs = inputs.split("\n\n")
    correct_order = []
    for i, (left, right) in enumerate(map(str.splitlines, pairs)):
        if PacketData(left) < PacketData(right):
            correct_order.append(i + 1)
    print(f"Part 1: {sum(correct_order)}")

    packets = list(map(PacketData, ("\n".join(pairs)).splitlines())) + DIVIDERS
    divider_indices = (sorted(packets).index(d) + 1 for d in DIVIDERS)
    print(f"Part 2: {math.prod(divider_indices)}\n")


solve(sample_input)
solve(actual_input)
