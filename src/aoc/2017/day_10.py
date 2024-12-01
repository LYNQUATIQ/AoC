import logging
import os
import re

from collections import defaultdict

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_10.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_txt = "165,1,255,31,87,52,24,113,0,91,148,254,158,2,73,153"


def get_hash_list(lengths, iterations=1):
    list_length = 256
    hash_list = {i: i for i in range(list_length)}
    current_position = 0
    skip_size = 0
    for _ in range(iterations):
        for length in lengths:
            sub_list = []
            for i in range(length):
                sub_list.append(hash_list[(current_position + i) % list_length])
            sub_list.reverse()
            for i in range(length):
                hash_list[(current_position + i) % list_length] = sub_list[i]
            current_position = (current_position + length + skip_size) % list_length
            skip_size += 1
    return hash_list


lengths = [int(l) for l in input_txt.split(",")]
hash_list = get_hash_list(lengths)

print(f"Part 1: {hash_list[0] * hash_list[1]}")

lengths = [ord(c) for c in input_txt] + [17, 31, 73, 47, 23]
hash_list = get_hash_list(lengths, 64)
dense_hash = []
for i in range(0, 256, 16):
    xor = hash_list[i]
    for n in range(1, 16):
        xor = xor ^ hash_list[i + n]
    dense_hash.append(xor)

hash_key = "".join([hex(h)[2:].zfill(2) for h in dense_hash])

print(f"Part 2: {hash_key}")
