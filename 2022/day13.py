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
        def _split_packet(packet: PacketData) -> tuple[PacketData, PacketData]:
            items = json.loads(packet)
            return (
                PacketData(str(items[0])),
                PacketData(str(list(i for i in items[1:]))),
            )

        assert isinstance(other, PacketData)
        if self == "[]" or other == "[]":
            return self == "[]"
        l_item, l_remaining = _split_packet(self)
        r_item, r_remaining = _split_packet(other)
        if l_item == r_item:
            return l_remaining < r_remaining
        if l_item.isdigit() and r_item.isdigit():
            return int(l_item) < int(r_item)
        if l_item.isdigit():
            return PacketData(f"[[{l_item}],{l_remaining}]") < other
        if r_item.isdigit():
            return self < PacketData(f"[[{r_item}],{r_remaining}]")
        return l_item < r_item


def solve(inputs: str) -> None:
    pairs = inputs.split("\n\n")
    packets = ("\n".join(pairs)).splitlines()

    correct_indices: list[int] = []
    for i, (left, right) in enumerate(map(str.splitlines, pairs), start=1):
        if PacketData(left) < PacketData(right):
            correct_indices.append(i)
    print(f"Part 1: {sum(correct_indices)}")

    DIVIDERS = [PacketData("[2]"), PacketData("[6]")]
    sorted_packets = sorted(list(map(PacketData, packets)) + DIVIDERS)
    divider_indices = (sorted_packets.index(d) + 1 for d in DIVIDERS)
    print(f"Part 2: {math.prod(divider_indices)}\n")


solve(sample_input)
solve(actual_input)
