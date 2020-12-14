import os

from collections import defaultdict
from utils import *

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

sample_input2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


class BitMaskDecoder:
    def __init__(self, inputs, floating_mode=False):
        self.floating_mode = floating_mode
        self.floating_bits = []
        self.memory = defaultdict(int)
        instructions = [line.split(" = ") for line in inputs.split("\n")]
        for token, value in instructions:
            if token == "mask":
                self.set_mask(value)
                continue
            register, value = int(token[4:-1]), int(value)
            if floating_mode:
                base_register = (register | self.mask_1) & ~sum(self.x_bits)
                for floating_bits in [sum(bits) for bits in powerset(self.x_bits)]:
                    self.memory[base_register + floating_bits] = value
            else:
                self.memory[register] = value | self.mask_1 & self.mask_0

    def memory_sum(self):
        return sum(self.memory.values())

    def set_mask(self, mask):
        self.x_bits = [2 ** i for i, b in enumerate(mask[::-1]) if b == "X"]
        self.mask_1 = int(mask.replace("X", "0"), 2)
        self.mask_0 = int(mask.replace("X", "1"), 2)


def solve(inputs1, inputs2):
    print(f"Part 1: {BitMaskDecoder(inputs1).memory_sum()}")
    print(f"Part 2: {BitMaskDecoder(inputs2, floating_mode=True).memory_sum()}\n")


solve(sample_input1, sample_input2)
solve(actual_input, actual_input)
