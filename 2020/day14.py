import os

from utils import powerset, print_time_taken


with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()

sample_input1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

sample_input2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


def decode_bitmask(inputs, floating_mode=False):
    memory = {}
    for token, value in [input_line.split(" = ") for input_line in inputs.split("\n")]:
        if token == "mask":
            x_bits = [2 ** i for i, b in enumerate(value[::-1]) if b == "X"]
            mask_1 = int(value.replace("X", "0"), 2)
            mask_0 = int(value.replace("X", "1"), 2)
            continue
        register, value = int(token[4:-1]), int(value)
        if floating_mode:
            base_register = (register | mask_1) & ~sum(x_bits)
            for floating_bits in powerset(x_bits):
                memory[base_register | sum(floating_bits)] = value
        else:
            memory[register] = (value | mask_1) & mask_0
    return sum(memory.values())


@print_time_taken
def solve(inputs1, inputs2):
    print(f"Part 1: {decode_bitmask(inputs1)}")
    print(f"Part 2: {decode_bitmask(inputs2, floating_mode=True)}\n")


solve(sample_input1, sample_input2)
solve(actual_input, actual_input)
