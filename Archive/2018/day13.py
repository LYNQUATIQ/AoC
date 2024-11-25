"""https://adventofcode.com/2018/day/13"""

import os

from itertools import cycle

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day13_input.txt")) as f:
    actual_input = f.read()

sample_input = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""


NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

TRACKS = {
    # Dict of directions... Enter coming from : Leave coming from
    "-": {EAST: EAST, WEST: WEST},
    "|": {NORTH: NORTH, SOUTH: SOUTH},
    "/": {SOUTH: WEST, EAST: NORTH, WEST: SOUTH, NORTH: EAST},
    "\\": {SOUTH: EAST, EAST: SOUTH, WEST: NORTH, NORTH: WEST},
    "+": {SOUTH: None, EAST: None, WEST: None, NORTH: None},
}

TRAINS = {
    # Tuple: Coming from, Track piece
    "v": (NORTH, "|"),
    "^": (SOUTH, "|"),
    "<": (EAST, "-"),
    ">": (WEST, "-"),
}


class Train:
    def __init__(self, origin, x, y):
        self.origin = origin
        self.x, self.y = x, y
        self.turn = cycle([-1, 0, 1])

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    @property
    def xy(self):
        return (self.x, self.y)

    def move(self, tracks):
        dx, dy = {NORTH: (0, 1), EAST: (-1, 0), SOUTH: (0, -1), WEST: (1, 0)}[
            self.origin
        ]
        self.x += dx
        self.y += dy

        new_direction = TRACKS[tracks[self.xy]][self.origin]
        if new_direction is None:
            new_direction = (self.origin + next(self.turn)) % 4
        self.origin = new_direction


@print_time_taken
def solve(inputs):
    tracks, trains = {}, set()
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c in TRAINS:
                origin, c = TRAINS[c]
                trains.add(Train(origin, x, y))
            if c in TRACKS:
                tracks[(x, y)] = c

    first_crash = None
    while len(trains) > 1:
        crashed_trains = set()
        for train in sorted(trains):
            train.move(tracks)
            try:
                crashed = next(t for t in trains if t != train and t.xy == train.xy)
            except StopIteration:
                continue
            first_crash = first_crash or train
            crashed_trains.update((train, crashed))
        trains = {t for t in trains if t not in crashed_trains}

    print(f"Part 1: {','.join(str(p) for p in first_crash.xy)}")
    print(f"Part 2: {','.join(str(p) for p in trains.pop().xy)}\n")


solve(sample_input)
solve(actual_input)
