"""https://adventofcode.com/2022/day/20"""
from __future__ import annotations
import os

from functools import lru_cache

with open(os.path.join(os.path.dirname(__file__), f"inputs/day20_input.txt")) as f:
    actual_input = f.read()


sample_input = """1
2
-3
3
-2
0
4"""


class Node:
    def __init__(self, value: int, prior_node: Node | None, next_node: Node | None):
        self.value = value
        self.prior_node: Node = prior_node or self
        self.next_node: Node = next_node or self

    def __repr__(self) -> str:
        return str(self.value)

    def nth_next(self, n: int) -> Node:
        node = self
        for _ in range(n):
            node = node.next_node
        return node

    def nth_prior(self, n: int) -> Node:
        node = self
        for _ in range(n):
            node = node.prior_node
        return node


DECRYPTION_KEY = 811589153


@lru_cache(maxsize=None)
def get_shift(n: int, cycle: int) -> int:
    return abs(n) % (cycle - 1)


def mix_coordinates(inputs: str, multiplier=1, iterations=1) -> int:
    zero_node = Node(-1, None, None)
    prior_node = Node(0, None, None)
    nodes: dict[int, Node] = {}
    for i, v in enumerate(map(int, inputs.splitlines())):
        this_node = Node(v * multiplier, prior_node, None)
        prior_node.next_node = this_node
        prior_node = this_node
        nodes[i] = this_node
        if v == 0:
            zero_node = this_node

    nodes[0].prior_node = prior_node
    this_node.next_node = nodes[0]
    file_length = len(nodes)
    assert zero_node.value == 0
    if file_length == 7:
        output = []
        n = zero_node
        for _ in range(file_length):
            output.append(str(n.value))
            n = n.next_node

    for i in range(iterations):
        for node in nodes.values():
            node.prior_node.next_node = node.next_node
            node.next_node.prior_node = node.prior_node
            shift = get_shift(abs(node.value), file_length)
            if node.value > 0:
                for _ in range(shift):
                    node.next_node = node.next_node.next_node
                node.prior_node = node.next_node.prior_node
            else:
                for _ in range(shift):
                    node.prior_node = node.prior_node.prior_node
                node.next_node = node.prior_node.next_node
            node.prior_node.next_node = node
            node.next_node.prior_node = node

        if file_length == 7:
            output = []
            n = zero_node
            for _ in range(file_length):
                output.append(str(n.value))
                n = n.next_node

    node = zero_node
    coordinates = 0
    for _ in range(3):
        node = node.nth_next(1000)
        coordinates += node.value
    return coordinates


from utils import print_time_taken


@print_time_taken
def solve(inputs: str) -> None:
    print(f"Part 1: {mix_coordinates(inputs)}")
    print(f"Part 2: {mix_coordinates(inputs,DECRYPTION_KEY, 10)}\n")


solve(sample_input)
solve(actual_input)
