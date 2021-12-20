"""https://adventofcode.com/2021/day/20"""
import os

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day20_input.txt")) as f:
    actual_input = f.read()

sample_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


BINARY_VALUE = {f"{x:03b}": x for x in range(8)}
BINARY_ENCODE = str.maketrans("#.", "10")
DARK, LIT = "0", "1"


def enhance_image(steps, image, algorithm, padding=DARK):
    for _ in range(steps):
        # Pad the image by two pixels for convenience
        image_size = len(image) + 4
        image = (
            [padding * image_size] * 2
            + [padding * 2 + raster + padding * 2 for raster in image]
            + [padding * image_size] * 2
        )

        # Adjust the padding (potentially changes state depending on algorithm)
        padding = algorithm[-1] if padding == LIT else algorithm[0]

        # Enhance the image (starting 1 pixel in from the padded image)
        enhanced_image = []
        for y in range(1, image_size - 1):
            raster = "".join(
                algorithm[
                    64 * BINARY_VALUE[image[y - 1][x - 1 : x + 2]]
                    + 8 * BINARY_VALUE[image[y][x - 1 : x + 2]]
                    + BINARY_VALUE[image[y + 1][x - 1 : x + 2]]
                ]
                for x in range(1, image_size - 1)
            )
            enhanced_image.append(raster)
        image = enhanced_image

    return image


@print_time_taken
def solve(inputs):
    algorithm, image_data = inputs.split("\n\n")

    # Encode the algorithm and image rasters (rows) into binary strings for convenience
    algorithm = algorithm.translate(BINARY_ENCODE)
    image = [raster.translate(BINARY_ENCODE) for raster in image_data.splitlines()]

    image = enhance_image(2, image, algorithm)
    print(f"Part 1: {sum(raster.count(LIT) for raster in image)}")

    image = enhance_image(48, image, algorithm)
    print(f"Part 2: {sum(raster.count(LIT) for raster in image)}\n")


solve(sample_input)
solve(actual_input)
