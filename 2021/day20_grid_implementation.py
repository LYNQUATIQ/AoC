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


BINARY_ENCODE = str.maketrans("#.", "10")
DARK, LIT = "0", "1"
DELTAS = list(product((-1, 0, 1), repeat=2))


def enhance_image(steps, image, algorithm, beyond=DARK):
    image_size = int(len(image) ** 0.5)
    for _ in range(steps):
        image_size += 2
        enhanced_image = {}
        for x, y in product(range(-1, image_size), range(-1, image_size)):
            index = "".join([image.get((x + dx, y + dy), beyond) for dy, dx in DELTAS])
            enhanced_image[(x + 1, y + 1)] = algorithm[int(index, 2)]
        image = enhanced_image
        beyond = algorithm[-1] if beyond == LIT else algorithm[0]
    return image


def solve(inputs):
    algorithm, image_data = inputs.split("\n\n")

    # Encode the algorithm and pixels into binary strings for convenience
    algorithm = algorithm.translate(BINARY_ENCODE)
    image = {
        (x, y): pixel
        for y, raster in enumerate(image_data.splitlines())
        for x, pixel in enumerate(raster.translate(BINARY_ENCODE))
    }

    image = enhance_image(2, image, algorithm)
    print(f"Part 1: {sum(pixel==LIT for pixel in image.values())}")

    image = enhance_image(48, image, algorithm)
    print(f"Part 2: {sum(pixel==LIT for pixel in image.values())}\n")


solve(sample_input)
solve(actual_input)
