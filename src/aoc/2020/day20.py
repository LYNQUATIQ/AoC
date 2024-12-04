import math
import os
import re


from collections import defaultdict
from itertools import product, combinations

from grid import XY
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day20_input.txt")) as f:
    actual_input = f.read()

example_input = """Tile 2311:
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

ROTATIONS = (0, 90, 180, 270)
FLIPPED = (True, False)
ORIENTATIONS = [orientation for orientation in product(FLIPPED, ROTATIONS)]

TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3
EDGE_DIRECTION = {XY(0, -1): TOP, XY(0, 1): BOTTOM, XY(1, 0): RIGHT, XY(-1, 0): LEFT}
CONNECTED_EDGE = {TOP: BOTTOM, RIGHT: LEFT, BOTTOM: TOP, LEFT: RIGHT}


class Tile:
    def __init__(self, tile_data, tile_id=None):
        self.id = tile_id
        self.size = len(tile_data)
        self.rows = [row for row in tile_data]
        self.cols = ["".join(row[i] for row in self.rows) for i in range(self.size)]

    @property
    def edge_values(self):
        edge_values = [self.rows[0], self.rows[-1], self.cols[0], self.cols[-1]]
        return tuple(edge_values + [s[::-1] for s in edge_values])

    def get_edge(self, edge):
        return {
            TOP: self.rows[0],
            RIGHT: self.cols[-1],
            BOTTOM: self.rows[-1],
            LEFT: self.cols[0],
        }[edge]

    def set_orientation(self, orientation):
        flipped, rotation = orientation
        if flipped:
            self.flip()
        for _ in range(rotation // 90):
            self.rotate()

    def flip(self):
        self.rows = [r[::-1] for r in self.rows]
        self.cols = self.cols[::-1]

    def rotate(self):
        self.rows = [col[::-1] for col in self.cols]
        self.cols = ["".join(row[i] for row in self.rows) for i in range(self.size)]

    def find_orientation(self, requirements):
        for orientation in ORIENTATIONS:
            rows_backup, cols_backup = self.rows[:], self.cols[:]
            self.set_orientation(orientation)
            edges = [self.get_edge(edge) for edge in (TOP, RIGHT, BOTTOM, LEFT)]
            self.rows, self.cols = rows_backup[:], cols_backup[:]
            if all(edges[e] == v for e, v in requirements):
                return orientation
        return None


@print_time_taken
def solve(inputs):
    grid = {}
    tiles = dict(
        (int(t[0].split()[1][:-1]), Tile(t[1:], int(t[0].split()[1][:-1])))
        for t in map(lambda x: x.splitlines(), inputs.split("\n\n"))
    )
    image_size, tile_size = int(len(tiles) ** 0.5), next(iter(tiles.values())).size

    # Find the neighbour for each tiles' sides
    neighbouring_tiles = {t: {} for t in tiles}
    for this_id, other_id in ((a, b) for a, b in product(tiles, tiles) if a != b):
        this, other = tiles[this_id], tiles[other_id]
        for edge in (s for s in other.edge_values if s in this.edge_values):
            neighbouring_tiles[this_id][edge] = other_id

    # Find corners - only have two neighbouring tiles (each with two orientations)
    corners = set(t for t in tiles if len(neighbouring_tiles[t]) == 4)
    print(f"Part 1: {math.prod(corners)}")

    # Assign one corner to top left orienting it so neignbours are to right and below
    corner_id = corners.pop()
    for right, bottom in combinations(neighbouring_tiles[corner_id], 2):
        orient = tiles[corner_id].find_orientation([(RIGHT, right), (BOTTOM, bottom)])
        if orient:
            tiles[corner_id].set_orientation(orient)

    # Loop until done finding tiles with matching edges to go in empty spaces
    grid[XY(0, 0)] = tiles.pop(corner_id)
    while tiles:
        xy, edge, empty_xy = None, None, None
        for xy in grid:
            neighbours = [n for n in xy.neighbours if n.in_bounds(image_size - 1)]
            spaces = [n for n in neighbours if n not in grid]
            if spaces:
                empty_xy = spaces[0]
                break
        edge_to_find = CONNECTED_EDGE[EDGE_DIRECTION[empty_xy - xy]]
        edge_value = grid[xy].get_edge(EDGE_DIRECTION[empty_xy - xy])
        tile = tiles[neighbouring_tiles[grid[xy].id][edge_value]]
        tile.set_orientation(tile.find_orientation([(edge_to_find, edge_value)]))
        grid[empty_xy] = tiles.pop(tile.id)

    # Consolidate grid tiles into a single image
    image_data = []
    for y, row in product(range(image_size), range(1, tile_size - 1)):
        raster = "".join(grid[(x, y)].rows[row][1:-1] for x in range(image_size))
        image_data.append(raster)

    # Search for sea monsters
    re1 = re.compile("..................#.")
    re2 = re.compile("#....##....##....###")
    re3 = re.compile(".#..#..#..#..#..#...")
    monsters = 0
    for orientation in ORIENTATIONS:
        image = Tile(image_data)
        image.set_orientation(orientation)
        for r in range(image.size - 2):
            r1, r2, r3 = image.rows[r], image.rows[r + 1], image.rows[r + 2]
            match = re1.search(r1)
            if match:
                while match:
                    if re2.match(r2, match.start()) and re3.match(r3, match.start()):
                        monsters += 1
                    match = re1.search(r1, match.start() + 1)

    print(f"Part 2: {sum(r.count('#') for r in image_data) - monsters * 15}\n")


solve(example_input)
solve(actual_input)
