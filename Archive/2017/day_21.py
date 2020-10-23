import logging
import os
import re

from collections import Counter

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_21.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_21_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

pattern = re.compile(r"^(?P<rule>[#./]+) => (?P<output>[#./]+)$")

two_by_two_rotate = {0: 3, 1: 0, 2: 2, 3: 4, 4: 1}  # ab/cd ==> ca/db
two_by_two_flips = [
    {0: 1, 1: 0, 2: 2, 3: 4, 4: 3},  # ab/cd ==> ba/dc
    {0: 3, 1: 4, 2: 2, 3: 0, 4: 1},  # ab/cd ==> cd/ab
]

# abc/def/ghi ==> gda/heb/ifc
three_by_three_rotate = {
    0: 8,
    1: 4,
    2: 0,
    3: 3,
    4: 9,
    5: 5,
    6: 1,
    7: 7,
    8: 10,
    9: 6,
    10: 2,
}
three_by_three_flips = [
    # abc/def/ghi ==> cba/fed/ihg
    {0: 2, 1: 1, 2: 0, 3: 3, 4: 6, 5: 5, 6: 4, 7: 7, 8: 10, 9: 9, 10: 8,},
    # abc/def/ghi ==> ghi/def/abc
    {0: 8, 1: 9, 2: 10, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 0, 9: 1, 10: 2,},
]

transforms = {
    5: (two_by_two_rotate, two_by_two_flips),
    11: (three_by_three_rotate, three_by_three_flips),
}


def do_transform(rule, transform):
    return "".join([rule[transform[i]] for i in range(len(rule))])


rules = {}
for line in lines:
    params = pattern.match(line).groupdict()
    rule = params["rule"]
    output = params["output"]
    rules[rule] = output
    rotate, flips = transforms[len(rule)]
    for flip in flips:
        rules[do_transform(rule, flip)] = output
    for _ in range(3):
        rule = do_transform(rule, rotate)
        rules[rule] = output


class Image:
    def __init__(self, rules):
        self.image = ".#./..#/###"
        self.rules = rules

    def tiles_from_image(self):
        rows = self.image.split("/")
        image_size = len(rows)
        tile_size = 2 + (len(rows) % 2 != 0)
        tiles = []
        for y1 in range(0, image_size, tile_size):
            for x in range(0, image_size, tile_size):
                tile_rows = []
                for y2 in range(tile_size):
                    y = y1 + y2
                    tile_rows.append(rows[y][x : x + tile_size])
                tiles.append("/".join(tile_rows))
        return tiles

    def set_image(self, tiles):
        tiles_per_row = int(len(tiles) ** 0.5)
        tile_size = 3 + (len(tiles[0]) == 19)
        image_size = tiles_per_row * tile_size
        rows = []
        for y in range(tiles_per_row):
            for y2 in range(tile_size):
                row = ""
                for x in range(tiles_per_row):
                    tile = tiles[y * tiles_per_row + x].split("/")
                    row += tile[y2]
                rows.append(row)
        self.image = "/".join(rows)

    def process_tile(self, tile):
        try:
            return self.rules[tile]
        except KeyError:
            pass

        rotate, flips = transforms[len(tile)]
        for flip in flips:
            try:
                return self.rules[do_transform(tile, flip)]
            except KeyError:
                pass

        for _ in range(3):
            tile = do_transform(tile, rotate)
            try:
                return self.rules[tile]
            except KeyError:
                pass

        raise NotImplementedError

    def process(self):
        tiles = self.tiles_from_image()
        processed_tiles = []
        for tile in tiles:
            processed_tiles.append(self.process_tile(tile))
        self.set_image(processed_tiles)

    def print_image(self):
        rows = self.image.split("/")
        print(f"\nImage size {len(rows)}")
        print(f"{self.image}\n")
        for row in rows:
            print(row)


image = Image(rules)
for _ in range(5):
    image.process()

print(f"Part 1: {Counter(image.image)['#']}")

for _ in range(13):
    image.process()

print(f"Part 2: {Counter(image.image)['#']}")

