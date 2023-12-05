"""https://adventofcode.com/2023/day/5"""
import os
import re

from itertools import chain

with open(os.path.join(os.path.dirname(__file__), "inputs/day05_input.txt")) as f:
    actual_input = f.read()


sample_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def get_mapped_range(
    range_start: int, range_length, item_map: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    if range_length == 0:
        return []
    for dest_start, source_start, length in item_map:
        if source_start <= range_start < source_start + length:
            offset = range_start - source_start
            range_found = min(length - offset, range_length)
            remainder = range_length - range_found
            return [(dest_start + offset, range_found)] + get_mapped_range(
                range_start + range_found, remainder, item_map
            )
        range_end = range_start + range_length - 1
        if source_start <= range_end < source_start + length:
            range_found = range_end - source_start + 1
            remainder = range_length - range_found
            return get_mapped_range(range_start, remainder, item_map) + [
                (dest_start, range_found)
            ]
    return [(range_start, range_length)]


def get_mapped_ranges(
    source_ranges: list[tuple[int, int]], item_map: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    destination_ranges = []
    for start, length in source_ranges:
        destination_ranges += get_mapped_range(start, length, item_map)
    return destination_ranges


def get_seed_locations(
    seed_ranges: list[tuple[int, int]], item_maps: list[list[tuple[int, int, int]]]
) -> list[int]:
    item_ranges = seed_ranges
    for item_map in item_maps:
        item_ranges = get_mapped_ranges(item_ranges, item_map)
    return [x[0] for x in list(chain(item_ranges))]


def solve(inputs):
    seeds_data, *maps_data = inputs.split("\n\n")
    seeds = [int(n) for n in re.findall(r"\d+", seeds_data)]
    item_maps = [
        [
            tuple(int(n) for n in re.findall(r"\d+", map_range))
            for map_range in map_data.splitlines()[1:]
        ]
        for map_data in maps_data
    ]

    seed_ranges = [(a, 1) for a in seeds]
    print(f"Part 1: {min(get_seed_locations(seed_ranges, item_maps))}")

    seed_ranges = [(a, b) for a, b in zip(seeds[0::2], seeds[1::2])]
    print(f"Part 2: {min(get_seed_locations(seed_ranges, item_maps))}\n")


solve(sample_input)
solve(actual_input)
