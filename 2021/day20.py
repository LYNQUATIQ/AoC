"""https://adventofcode.com/2021/day/20"""
import os
from itertools import product

with open(os.path.join(os.path.dirname(__file__), f"inputs/day20_input.txt")) as f:
    actual_input = f.read()

sample_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

NOT_LIT, LIT = ".", "#"


def enhanced_image(steps, image_data, algorithm):
    pixels = set()
    for y, row in enumerate(image_data.splitlines()):
        for x, pixel in enumerate(row):
            if pixel == LIT:
                pixels.add((x, y))

    image_size = x + 1
    off_image_lit = False
    for _ in range(steps):
        output_pixels = set()
        for x, y in product(range(-1, image_size + 1), range(-1, image_size + 1)):
            algo_index = 0
            for yi, xi in product(range(y - 1, y + 2), range(x - 1, x + 2)):
                if 0 <= xi < image_size and 0 <= yi < image_size:
                    lit = (xi, yi) in pixels
                else:
                    lit = off_image_lit
                algo_index = algo_index * 2 + (1 if lit else 0)
            if algorithm[algo_index]:
                output_pixels.add((x + 1, y + 1))
        off_image_lit = algorithm[-1] if off_image_lit else algorithm[0]
        image_size += 2
        pixels = output_pixels
    return pixels


def solve(inputs):
    algorithm, rasters = inputs.split("\n\n")
    algorithm = tuple(a == LIT for a in algorithm)

    print(f"Part 1: {len(enhanced_image(2, rasters, algorithm))}")
    print(f"Part 2: {len(enhanced_image(50, rasters, algorithm))}\n")


solve(sample_input)
solve(actual_input)
