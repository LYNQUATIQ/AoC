# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter
from itertools import product

from grid import XY, ConnectedGrid
from utils import flatten, grouper, powerset, print_time_taken

# log_file = os.path.join(os.path.dirname(__file__), f"logs/day13.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
with open(os.path.join(os.path.dirname(__file__), f"inputs/day13_input.txt")) as f:
    actual_input = f.read()

sample_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


@print_time_taken
def solve(inputs):
    dot_inputs, fold_inputs = inputs.split("\n\n")

    dots = set()
    for xy in dot_inputs.splitlines():
        x, y = xy.split(",")
        dots.add((int(x), int(y)))

    folds = []
    for line in fold_inputs.splitlines():
        fold_xy, value = line.split()[-1].split("=")
        folds.append((fold_xy, int(value)))

    def do_fold(dots, xy, value):
        new_dots = set()
        for x, y in dots:
            if xy == "x" and x >= value:
                x = 2 * value - x
            if xy == "y" and y >= value:
                y = 2 * value - y
            new_dots.add((x, y))
        return new_dots

    dots = do_fold(dots, *folds[0])
    print(f"Part 1: {len(dots)}")

    for fold in folds[1:]:
        dots = do_fold(dots, *fold)
    print(f"Part 2:\n")
    max_x, max_y = max(xy[0] for xy in dots), max(xy[1] for xy in dots)
    for y in range(max_y + 1):
        print("".join("\u2588" if (x, y) in dots else " " for x in range(max_x + 1)))


solve(sample_input)
solve(actual_input)
