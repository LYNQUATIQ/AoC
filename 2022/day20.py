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
    file_data = inputs.splitlines()
    file_length = len(file_data)

    node_values: list[int] = [0] * file_length
    next_node_index: list[int] = [0] * file_length
    prior_node_index: list[int] = [0] * file_length

    for i, v in enumerate(map(int, file_data)):
        node_values[i] = v * multiplier
        next_node_index[i] = (i + 1) % file_length
        prior_node_index[i] = (i - 1) % file_length
        if v == 0:
            zero_node_index = i

    def print_values():
        print(
            ", ".join(
                str(node_values[ni])
                for ni in [next_node_index[-1]] + next_node_index[:-1]
            ),
        )

    print("Initial arraangement")
    print_values()

    for _ in range(iterations):
        for i, value in enumerate(node_values):
            print("Moving ", value)
            next_index, prior_index = next_node_index[i], prior_node_index[i]
            next_node_index[prior_index] = next_index
            prior_node_index[next_index] = prior_index
            print_values()
            shift = abs(value) % (file_length - 1)
            if value > 0:
                for _ in range(shift):
                    next_node_index[i] = next_node_index[next_node_index[i]]
                prior_node_index[i] = prior_node_index[next_node_index[i]]
            else:
                for _ in range(shift):
                    prior_node_index[i] = prior_node_index[prior_node_index[i]]
                next_node_index[i] = next_node_index[next_node_index[i]]
            next_node_index[prior_node_index[i]] = i
            prior_node_index[next_node_index[i]] = i
            print_values()

    i = zero_node_index
    coordinates = 0
    for _ in range(3):
        for _ in range(1000):
            i = next_node_index[i]
        coordinates += node_values[i]
    return coordinates


@print_time_taken
def solve(inputs: str) -> None:
    print(f"Part 1: {mix_coordinates(inputs)}")
    # print(f"Part 2: {mix_coordinates(inputs,DECRYPTION_KEY, 10)}\n")


solve(sample_input)
# solve(actual_input)
