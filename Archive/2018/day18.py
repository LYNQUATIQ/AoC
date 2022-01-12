"""https://adventofcode.com/2018/day/18"""
import os

from itertools import chain, product
from typing import NamedTuple

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day18_input.txt")) as f:
    actual_input = f.read()

sample_input = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

GROUND, TREE, LUMBERYARD = ".", "|", "#"


class XY(NamedTuple("Pt", [("x", int), ("y", int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    @property
    def neighbours(self):
        for direction in list(product((-1, 0, 1), (-1, 0, 1))):
            if not all(d == 0 for d in direction):
                yield self + type(self)(*direction)


def update_trees_lumberyards(
    trees: frozenset[XY], lumberyards: frozenset[XY], max_x: int, max_y: int
) -> tuple[frozenset[XY], frozenset[XY]]:
    # Focus on neighbours of trees - if they're open they might become a tree;
    # if they're a lumberyard they might potentially stay as lumberyards
    tree_neighbours = {xy: list(xy.neighbours) for xy in trees}
    candidates = list(
        xy
        for xy in chain.from_iterable(tree_neighbours.values())
        if xy not in trees and 0 <= xy.x < max_x and 0 <= xy.y < max_y
    )

    # Change trees to lumberyards if they have at least three lumberyard neighbours
    # (otherwise they stay as trees)
    new_lumberyards = {
        tree_xy
        for tree_xy in trees
        if sum(xy in lumberyards for xy in tree_neighbours[tree_xy]) >= 3
    }
    new_trees = set(xy for xy in trees if xy not in new_lumberyards)

    # Keep lumberyards (next to trees) if they have also neighbour another lumberyard
    for lumberyard_xy in (xy for xy in candidates if xy in lumberyards):
        if any(n in lumberyards for n in lumberyard_xy.neighbours):
            new_lumberyards.add(lumberyard_xy)

    # Change open areas (next to trees) to trees if they've at least 3 tree neighbours
    for open_xy in (xy for xy in candidates if xy not in lumberyards):
        if sum(xy in trees for xy in open_xy.neighbours) >= 3:
            new_trees.add(open_xy)

    return frozenset(new_trees), frozenset(new_lumberyards)


@print_time_taken
def solve(inputs):
    trees, lumberyards = set(), set()
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == TREE:
                trees.add(XY(x, y))
            elif c == LUMBERYARD:
                lumberyards.add(XY(x, y))
    max_x, max_y = x + 1, y + 1

    trees, lumberyards = frozenset(trees), frozenset(lumberyards)
    for _ in range(10):
        trees, lumberyards = update_trees_lumberyards(trees, lumberyards, max_x, max_y)
    print(f"Part 1: {len(trees) * len(lumberyards)}")

    minute = 10
    states = {}
    while True:
        states[(trees, lumberyards)] = minute
        trees, lumberyards = update_trees_lumberyards(trees, lumberyards, max_x, max_y)
        minute += 1
        if (trees, lumberyards) in states:
            break

    cycle_base = states[(trees, lumberyards)]
    cycle_length = minute - cycle_base
    for _ in range((1_000_000_000 - cycle_base) % cycle_length):
        trees, lumberyards = update_trees_lumberyards(trees, lumberyards, max_x, max_y)
    print(f"Part 2: {len(trees) * len(lumberyards)}\n")


solve(sample_input)
solve(actual_input)
