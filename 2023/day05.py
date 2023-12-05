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

ITEMS = ["soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]


def get_mapped_range(
    range_start: int, range_length, mappings: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    if range_length == 0:
        return []
    for dest_start, source_start, length in mappings:
        if source_start <= range_start < source_start + length:
            offset = range_start - source_start
            length -= offset
            range_found = min(length, range_length)
            remainder = range_length - range_found
            return [
                (dest_start + offset, min(length, range_length))
            ] + get_mapped_range(range_start + range_found, remainder, mappings)
        range_end = range_start + range_length - 1
        if source_start <= range_end < source_start + length:
            range_found = range_end - source_start + 1
            remainder = range_length - range_found
            return get_mapped_range(range_start, remainder, mappings) + [
                (dest_start, range_found)
            ]

    return [(range_start, range_length)]


def get_mapped_ranges(
    sources: list[tuple[int, int]], mappings: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    destinations = []
    for start, length in sources:
        destinations += get_mapped_range(start, length, mappings)
    return destinations


def get_seed_locations(
    seed_ranges: list[tuple[int, int]], item_maps: dict[str, list[tuple[int, int, int]]]
) -> list[int]:
    item_ranges = seed_ranges
    for item in ITEMS:
        item_ranges = get_mapped_ranges(item_ranges, item_maps[item])
    return [x[0] for x in list(chain(item_ranges))]


def solve(inputs):
    seeds_data, *maps_data = inputs.split("\n\n")

    seeds = list(map(int, re.findall(r"\d+", seeds_data)))
    item_maps = {}
    for map_data in maps_data:
        label, *mappings = map_data.splitlines()
        map_key = label.split()[0].split("-to-")[1]
        item_maps[map_key] = [
            tuple(map(int, re.findall(r"\d+", mapping))) for mapping in mappings
        ]

    seed_ranges = [(a, 1) for a in seeds]
    locations = get_seed_locations(seed_ranges, item_maps)
    print(f"Part 1: {min(locations)}")

    seed_ranges = [(a, b) for a, b in zip(seeds[0::2], seeds[1::2])]
    locations = get_seed_locations(seed_ranges, item_maps)
    print(f"Part 2: {min(locations)}\n")


solve(sample_input)
solve(actual_input)
