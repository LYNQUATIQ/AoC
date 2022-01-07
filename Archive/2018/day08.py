"""https://adventofcode.com/2018/day/8"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day08_input.txt")) as f:
    actual_input = f.read()

sample_input = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"""


class DataStream:
    def __init__(self, input_data: list[int]) -> None:
        self.data_stream = input_data
        self.pointer: int = 0

    def read_value(self) -> int:
        value = self.data_stream[self.pointer]
        self.pointer += 1
        return value


class Node:
    def __init__(self, data_stream: DataStream) -> None:
        num_children, num_meta_data = data_stream.read_value(), data_stream.read_value()
        self.children = [Node(data_stream) for _ in range(num_children)]
        self.meta_data = [data_stream.read_value() for _ in range(num_meta_data)]

    @property
    def meta_data_sum(self):
        return sum(c.meta_data_sum for c in self.children) + sum(self.meta_data)

    @property
    def value(self):
        if not self.children:
            return self.meta_data_sum
        return sum(
            self.children[i - 1].value
            for i in self.meta_data
            if 0 < i <= len(self.children)
        )


def solve(inputs):
    root_node = Node(DataStream(list(map(int, inputs.split()))))
    print(f"Part 1: {root_node.meta_data_sum}")
    print(f"Part 2: {root_node.value}\n")


solve(sample_input)
solve(actual_input)
