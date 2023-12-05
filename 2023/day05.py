"""https://adventofcode.com/2023/day/5"""
import os
import re


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


def solve(inputs):
    seeds_data, *maps_data = inputs.split("\n\n")

    seeds = list(map(int, re.findall(r"\d+", seeds_data)))
    maps = {}
    for map_data in maps_data:
        label, *mappings = map_data.splitlines()
        map_key = label.split()[0].split("-to-")[1]
        maps[map_key] = [
            tuple(map(int, re.findall(r"\d+", mapping))) for mapping in mappings
        ]

    locations = []
    for seed in seeds:
        item_key = seed
        for item in ITEMS:
            next_item = item_key
            for dest, source, length in maps[item]:
                if source <= item_key < source + length:
                    next_item = dest + item_key - source
                    break
            item_key = next_item
        locations.append(item_key)
    print(f"Part 1: {min(locations)}")

    seed_ranges = [(a, b) for a, b in zip(seeds[0::2], seeds[1::2])]

    location = 0
    while True:
        item_key = location
        for item in ITEMS[::-1]:
            for dest, source, length in maps[item]:
                if dest <= item_key < dest + length:
                    item_key = source + item_key - dest
                    break
        if any(a <= item_key < a + b for a, b in seed_ranges):
            break
        location += 1
    print(f"Part 2: {location}\n")


solve(sample_input)
solve(actual_input)
