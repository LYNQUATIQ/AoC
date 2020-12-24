import os

from collections import defaultdict

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day24_input.txt")) as f:
    actual_input = f.read()

sample_input = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


class TileFloor:
    DIRECTIONS = {
        "e": (2, 0),
        "se": (1, 1),
        "sw": (-1, 1),
        "w": (-2, 0),
        "nw": (-1, -1),
        "ne": (1, -1),
    }
    BLACK, WHITE = True, False

    def tile_neighbours(self, tile):
        return ((tile[0] + d[0], tile[1] + d[1]) for d in self.DIRECTIONS.values())

    def __init__(self, instructions):
        self.grid = defaultdict(lambda: self.WHITE)
        for instruction in instructions:
            tile = (0, 0)
            i = 0
            while i < len(instruction):
                direction = instruction[i]
                i += 1
                if direction in ["s", "n"]:
                    direction += instruction[i]
                    i += 1
                d = self.DIRECTIONS[direction]
                tile = (tile[0] + d[0], tile[1] + d[1])
            self.grid[tile] = not self.grid[tile]

    def iterate(self, rounds):
        black_tiles = set(tile for tile in self.grid if self.grid[tile] == self.BLACK)
        for _ in range(rounds):
            new_black_tiles = set()
            for t in black_tiles.union(*(self.tile_neighbours(t) for t in black_tiles)):
                n_count = sum(n in black_tiles for n in self.tile_neighbours(t))
                if n_count in [1, 2] and (n_count == 2 or t in black_tiles):
                    new_black_tiles.add(t)
            black_tiles = new_black_tiles
        return len(black_tiles)


@print_time_taken
def solve(inputs):
    floor = TileFloor(inputs.splitlines())

    print(f"Part 1: {sum(floor.grid.values())}")
    print(f"Part 2: {floor.iterate(100)}\n")


solve(sample_input)
solve(actual_input)
