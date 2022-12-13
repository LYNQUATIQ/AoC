"""https://adventofcode.com/2022/day/13"""
from __future__ import annotations

import json
import math
import os

from functools import total_ordering

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


@total_ordering
class PacketData:
    def __init__(self, data: str) -> None:
        self._data = data

    def __repr__(self) -> str:
        return str(self._data)

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, PacketData)
        return self._data == other._data

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, PacketData)
        if self.is_empty or other.is_empty:
            return self.is_empty
        l_item, l_remaining = PacketData._split_packet(self)
        r_item, r_remaining = PacketData._split_packet(other)
        if l_item == r_item:
            return l_remaining < r_remaining
        if l_item.is_integer and r_item.is_integer:
            return int(l_item._data) < int(r_item._data)
        if l_item.is_integer:
            return PacketData(f"[[{l_item}],{l_remaining}]") < other
        if r_item.is_integer:
            return self < PacketData(f"[[{r_item}],{r_remaining}]")
        return l_item < r_item

    @property
    def is_integer(self) -> bool:
        return self._data.isdigit()

    @property
    def is_empty(self) -> bool:
        return self._data == "[]"

    @staticmethod
    def _split_packet(packet: PacketData) -> tuple[PacketData, PacketData]:
        items = json.loads(packet._data)
        return (
            PacketData(str(items[0])),
            PacketData(str(list(i for i in items[1:]))),
        )


def solve(inputs: str) -> None:
    pairs = inputs.split("\n\n")

    correct_indices: list[int] = []
    for i, (left, right) in enumerate(map(str.splitlines, pairs), start=1):
        if PacketData(left) < PacketData(right):
            correct_indices.append(i)
    print(f"Part 1: {sum(correct_indices)}")

    DIVIDERS = ("[2]", "[6]")
    packets = ("\n".join(pairs)).splitlines() + list(DIVIDERS)
    sorted_packets = [str(p) for p in sorted(list(map(PacketData, packets)))]
    divider_indices = (sorted_packets.index(d) + 1 for d in DIVIDERS)
    print(f"Part 2: {math.prod(divider_indices)}\n")


solve(sample_input)
solve(actual_input)
