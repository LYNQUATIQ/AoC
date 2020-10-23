import logging
import os

from collections import defaultdict


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

assert (len(lines) == 1)

compressed = lines[0]

def decompressed_length(compressed, recurse=False):
    total_length = 0
    pointer = 0
    while pointer < len(compressed):
        if compressed[pointer] != "(":
            total_length += 1
            pointer += 1
            continue

        end_marker = compressed.find(")", pointer)
        marker = compressed[pointer+1:end_marker]
        string_length, rep = (int(n) for n in marker.split("x"))
        pointer = end_marker + 1
        if recurse:
            total_length += decompressed_length(compressed[pointer:pointer+string_length], recurse) * rep
        else:
            total_length += string_length * rep
        pointer += string_length

    return total_length

print(f"Part 1: {decompressed_length(compressed)}")
print(f"Part 2: {decompressed_length(compressed, True)}")

