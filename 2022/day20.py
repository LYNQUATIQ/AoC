"""https://adventofcode.com/2022/day/20"""
from __future__ import annotations
import os

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day20_input.txt")) as f:
    actual_input = f.read()


sample_input = """1
2
-3
3
-2
0
4"""

DECRYPTION_KEY = 811589153


class Node:
    def __init__(self, value: int, prior_node: Node | None, next_node: Node | None):
        self.value = value
        self.prior_node: Node = prior_node or self
        self.next_node: Node = next_node or self


def mix_coordinates(inputs: str, multiplier=1, iterations=1) -> int:
    zero_node = Node(-1, None, None)
    prior_node = Node(0, None, None)
    nodes: list[Node] = []
    for v in map(int, inputs.splitlines()):
        this_node = Node(v * multiplier, prior_node, None)
        prior_node.next_node = this_node
        prior_node = this_node
        nodes.append(this_node)
        if v == 0:
            zero_node = this_node
    nodes[0].prior_node = prior_node
    this_node.next_node = nodes[0]
    file_length = len(nodes)

    for i in range(iterations):
        for node in nodes:
            node.prior_node.next_node = node.next_node
            node.next_node.prior_node = node.prior_node
            shift = abs(node.value) % (file_length - 1)
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

    node = zero_node
    coordinates = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.next_node
        coordinates += node.value
    return coordinates


@print_time_taken
def solve(inputs: str) -> None:
    print(f"Part 1: {mix_coordinates(inputs)}")
    print(f"Part 2: {mix_coordinates(inputs,DECRYPTION_KEY, 10)}\n")


solve(sample_input)
solve(actual_input)
