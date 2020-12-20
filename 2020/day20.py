import math
import os
import re


from collections import defaultdict
from itertools import product, combinations

from grid import XY
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day20_input.txt")) as f:
    actual_input = f.read()

sample_input = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3
BORDERS = (TOP, RIGHT, BOTTOM, LEFT)
ROTATIONS = (0, 90, 180, 270)
ORIENTATIONS = [orientation for orientation in product((False, True), ROTATIONS)]

EDGE_DIRECTION = {XY(0, -1): TOP, XY(0, 1): BOTTOM, XY(1, 0): RIGHT, XY(-1, 0): LEFT}
CONNECTED_EDGE = {TOP: BOTTOM, RIGHT: LEFT, BOTTOM: TOP, LEFT: RIGHT}


class Tile:
    def __init__(self, tile_id, tile_data):
        self.size = len(tile_data)
        self.id = tile_id
        self.rows = [row for row in tile_data]
        self.cols = ["".join(row[i] for row in self.rows) for i in range(self.size)]

    @property
    def border_values(self):
        border_values = [self.rows[0], self.rows[-1], self.cols[0], self.cols[-1]]
        return tuple(border_values + [s[::-1] for s in border_values])

    def get_edge(self, border):
        return {
            TOP: self.rows[0],
            RIGHT: self.cols[-1],
            BOTTOM: self.rows[-1],
            LEFT: self.cols[0],
        }[border]

    def find_orientation(self, requirements):
        for orientation in ORIENTATIONS:
            rows_backup, cols_backup = self.rows[:], self.cols[:]
            self.set_orientation(orientation)
            edges = [self.get_edge(edge) for edge in BORDERS]
            self.rows, self.cols = rows_backup[:], cols_backup[:]
            if all(edges[e] == v for e, v in requirements):
                return orientation
        return None

    def flip(self):
        self.rows = [r[::-1] for r in self.rows]
        self.cols = self.cols[::-1]

    def rotate(self):
        self.rows = [col[::-1] for col in self.cols]
        self.cols = ["".join(row[i] for row in self.rows) for i in range(self.size)]

    def set_orientation(self, orientation):
        flipped, rotation = orientation
        if flipped:
            self.flip()
        for _ in range(rotation // 90):
            self.rotate()


@print_time_taken
def solve(inputs):
    grid = {}
    tiles = set(
        Tile(int(t[0].split()[1][:-1]), t[1:])
        for t in map(lambda x: x.splitlines(), inputs.split("\n\n"))
    )
    tiles = {t.id: t for t in tiles}
    image_size = int(len(tiles) ** 0.5)

    # Find all possible neighbours for each tiles' sides
    possible_neighbours = {t: defaultdict(set) for t in tiles}
    for this, other in (
        (tiles[a], tiles[b]) for a, b in product(tiles, tiles) if a != b
    ):
        for border in (s for s in other.border_values if s in this.border_values):
            possible_neighbours[this.id][border].add(other.id)

    # Find corners - only have neighbours on two side (each side has two orientations)
    corners = set(t for t in tiles if len(possible_neighbours[t]) == 4)
    print(f"Part 1: {math.prod(corners)}")

    # Assign one corner to top left and orient it so neignbours are to right and below
    top_corner = tiles[corners.pop()]
    for right, bottom in combinations(possible_neighbours[top_corner.id], 2):
        orientation = top_corner.find_orientation([(RIGHT, right), (BOTTOM, bottom)])
        if orientation:
            top_corner.set_orientation(orientation)

    # Find tile with empty space next to it and look for neighbour with matching edge
    grid[XY(0, 0)] = tiles.pop(top_corner.id)
    while tiles:
        xy, edge, empty_xy, found_tile = None, None, None, None
        for xy in grid:
            spaces = [
                n
                for n in xy.neighbours
                if n.in_bounds(image_size - 1) and n not in grid
            ]
            if spaces:
                empty_xy = spaces[0]
                edge = EDGE_DIRECTION[empty_xy - xy]
                break
        edge_value = grid[xy].get_edge(edge)
        edge_to_find, value_to_find = CONNECTED_EDGE[edge], edge_value
        for tile in tiles.values():
            orientation = tile.find_orientation([(edge_to_find, value_to_find)])
            if orientation:
                tile.set_orientation(orientation)
                found_tile = tile
                break
        grid[empty_xy] = tiles.pop(found_tile.id)

    # Consolidate grid tiles into a single image
    image_data = []
    for y, row in product(range(image_size), range(1, top_corner.size - 1)):
        raster = "".join(grid[(x, y)].rows[row][1:-1] for x in range(image_size))
        image_data.append(raster)

    # Search for sea monsters
    re1 = re.compile("..................#.")
    re2 = re.compile("#....##....##....###")
    re3 = re.compile(".#..#..#..#..#..#...")
    monsters = 0
    for orientation in ORIENTATIONS:
        image = Tile(1, image_data)
        image.set_orientation(orientation)
        for r in range(0, image.size - 2):
            r1, r2, r3 = image.rows[r], image.rows[r + 1], image.rows[r + 2]
            match = re2.search(r2)
            if match:
                while True:
                    if re1.match(r1, match.start()) and re3.match(r3, match.start()):
                        monsters += 1
                    match = re2.search(r2, match.start() + 1)
                    if not match:
                        break

    print(f"Part 2: {sum(r.count('#') for r in image_data) - monsters * 15}\n")


solve(sample_input)
solve(actual_input)
