"""https://adventofcode.com/2022/day/13"""
from __future__ import annotations
import math
import os

from ast import literal_eval
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
    class PacketsEqual(Exception):
        """Raised when packets are equal (same value or empty lists)"""

    def __init__(self, data: str) -> None:
        self._data = data

    def __repr__(self) -> str:
        return str(self._data)

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, PacketData)
        if self.is_integer and other.is_integer:
            return self._data == other._data
        elif self.is_list and other.is_list:
            return self.empty and other.empty
        return False

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, PacketData)
        try:
            return PacketData._compare(self, other)
        except PacketData.PacketsEqual:
            return False

    @property
    def is_integer(self) -> bool:
        return self._data.isdigit()

    @property
    def is_list(self) -> bool:
        return not self.is_integer

    @property
    def empty(self) -> bool:
        assert not self.is_integer
        return self._data == "[]"

    @staticmethod
    def _split_packet(packet: PacketData) -> tuple[PacketData, PacketData]:
        items = literal_eval(packet._data)
        return (
            PacketData(str(items[0])),
            PacketData(str(list(i for i in items[1:]))),
        )

    @staticmethod
    def _combine_packet(item: PacketData, other: PacketData) -> PacketData:
        item_str = str(f"[{item}]") if item.is_integer else str(item)
        items = [item_str] + literal_eval(other._data)
        return PacketData(str(list(i for i in items)))

    @staticmethod
    def _compare(left_packet: PacketData, right_packet: PacketData) -> bool:
        if left_packet == right_packet:
            raise PacketData.PacketsEqual

        if left_packet.empty or right_packet.empty:
            return left_packet.empty

        l_item, l_remaining = PacketData._split_packet(left_packet)
        r_item, r_remaining = PacketData._split_packet(right_packet)

        if l_item == r_item:
            return PacketData._compare(l_remaining, r_remaining)
        if l_item.is_integer and r_item.is_integer:
            return int(l_item._data) < int(r_item._data)
        if l_item.is_integer or r_item.is_integer:
            return PacketData._compare(
                PacketData._combine_packet(l_item, l_remaining),
                PacketData._combine_packet(r_item, r_remaining),
            )
        # Both items are lists
        if l_item.empty and not r_item.empty:
            return True
        if r_item.empty and not l_item.empty:
            return False
        try:
            return PacketData._compare(l_item, r_item)
        except PacketData.PacketsEqual:
            return PacketData._compare(l_remaining, r_remaining)


DIVIDERS = ("[2]", "[6]")


def solve(inputs: str) -> None:
    pairs = inputs.split("\n\n")

    correct_indices: list[int] = []
    for i, (l, r) in enumerate(map(str.splitlines, pairs), start=1):
        left, right = PacketData(l), PacketData(r)
        if left < right:
            correct_indices.append(i)
    print(f"Part 1: {sum(correct_indices)}")

    packet_data = "\n".join(pairs) + "\n" + "\n".join(DIVIDERS)
    packets = list(map(PacketData, packet_data.splitlines()))
    packets.sort()
    packet_strings = [str(p) for p in packets]
    divider_indices = (packet_strings.index(d) + 1 for d in DIVIDERS)

    print(f"Part 2: {math.prod(divider_indices)}\n")


solve(sample_input)
solve(actual_input)
