import logging
import os

from math import log2

from grid_system import ConnectedGrid, XY


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_14.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)


def get_hash_list(lengths, iterations=64):
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


def get_hash_key(input_string):
    lengths = [ord(c) for c in input_string] + [17, 31, 73, 47, 23]
    hash_list = get_hash_list(lengths, 64)
    dense_hash = []
    for i in range(0, 256, 16):
        xor = hash_list[i]
        for n in range(1, 16):
            xor = xor ^ hash_list[i + n]
        dense_hash.append(xor)
    hash_key = "".join([hex(h)[2:].zfill(2) for h in dense_hash])
    return hash_key


def hex_to_bitstream(hex_value):
    num_of_bits = int(len(hex_value) * log2(16))
    return bin(int(hex_value, 16))[2:].zfill(num_of_bits)


input_txt = "wenycdww"
# input_txt = "flqrgnkx"

disk = ConnectedGrid()
blocks = 0
for y in range(128):
    hash_key = get_hash_key(f"{input_txt}-{str(y)}")
    bitstream = hex_to_bitstream(hash_key)
    for x, c in enumerate(bitstream):
        if c == "1":
            blocks += 1
        disk.grid[XY(x, y)] = {"1": "#", "0": "."}[c]

print(f"Part 1: {blocks}")

disk.print_grid()

block_regions = {}
regions = {}
region_counter = 1
for y in range(128):
    for x in range(128):
        block = XY(x, y)
        if disk.grid[block] == ".":
            continue
        try:
            region = block_regions[block]
        except KeyError:
            region = region_counter
            region_counter += 1
            regions[region] = set([block])
            block_regions[block] = region

        adjacent_blocks = [n for n in block.neighbours if disk.grid.get(n, 0) == "#"]
        for adjacent_block in adjacent_blocks:
            try:
                existing_region = block_regions[adjacent_block]
            except KeyError:
                regions[region].add(adjacent_block)
                block_regions[adjacent_block] = region
                continue

            if existing_region == region:
                continue

            for b in regions[existing_region]:
                regions[region].add(b)
                block_regions[b] = region

            del regions[existing_region]

print(f"Part 2: {len(regions)}")
