"""https://adventofcode.com/2021/day/20"""
import os
from collections import deque

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day20_input.txt")) as f:
    actual_input = f.read()

sample_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


BINARY = {f"{x:03b}": x for x in range(8)}
DECODE = str.maketrans("#.", "10")
ENCODE = str.maketrans("10", "#.")


def enhanced_pixel_count(steps, image_data, algorithm):
    rasters = deque(r.translate(DECODE) for r in image_data.splitlines())
    image_size = len(rasters)

    padding = "0"
    for _ in range(steps):
        image_size = len(rasters) + 4
        rasters = deque((padding * 2 + r + padding * 2 for r in rasters))
        rasters.extendleft([padding * image_size] * 2)
        rasters.extend([padding * image_size] * 2)

        padding = algorithm[-1] if padding == "1" else algorithm[0]
        enhanced_rasters = deque()
        for y in range(1, image_size - 1):
            raster = "".join(
                algorithm[
                    64 * BINARY[rasters[y - 1][x - 1 : x + 2]]
                    + 8 * BINARY[rasters[y][x - 1 : x + 2]]
                    + BINARY[rasters[y + 1][x - 1 : x + 2]]
                ]
                for x in range(1, image_size - 1)
            )
            enhanced_rasters.append(raster)
        rasters = enhanced_rasters

    return sum(r.count("1") for r in rasters)


@print_time_taken
def solve(inputs):
    algorithm, image_data = inputs.split("\n\n")
    algorithm = tuple(str(int(a == "#")) for a in algorithm)

    print(f"Part 1: {enhanced_pixel_count(2, image_data, algorithm)}")
    print(f"Part 2: {enhanced_pixel_count(50, image_data, algorithm)}\n")


solve(sample_input)
solve(actual_input)
