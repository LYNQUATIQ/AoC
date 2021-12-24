"""https://adventofcode.com/2021/day/24"""
import logging
import math
import os
import re
import string

from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
from itertools import product
from functools import cache, lru_cache

from grid import XY, ConnectedGrid
from utils import flatten, grouper, powerset, print_time_taken

log_file = os.path.join(os.path.dirname(__file__), f"logs/day24.log")
logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w")
with open(os.path.join(os.path.dirname(__file__), f"inputs/day24_input.txt")) as f:
    actual_input = f.read()

PARAMS = [
    (1, 14, 14),
    (1, 14, 2),
    (1, 14, 11),
    (1, 12, 13),
    (1, 15, 5),
    (26, -12, 5),
    (26, -12, 5),
    (1, 12, 9),
    (26, -7, 3),
    (1, 13, 13),
    (26, -8, 2),
    (26, -5, 1),
    (26, -10, 11),
    (26, -7, 8),
]


@lru_cache
def get_next_z(digit: int, z: int, z_div, constant1, constant2) -> int:
    x = z % 26
    z = z // z_div
    x += constant1
    x = int(x != digit)
    y = 25 * x + 1
    z *= y
    y = digit + constant2
    y *= x
    return z + y


@print_time_taken
def solve(inputs):

    model_number, delta = 99999999999999, -1
    while True:
        model_number += delta
        while "0" in str(model_number):
            model_number += delta
        z = 0
        for digit, params in zip(str(model_number), PARAMS):
            z = get_next_z(int(digit), z, *params)
        if z == 0:
            break

    print(f"Part 1: {model_number}")

    model_number, delta = 11111111111111, +1
    while True:
        model_number += delta
        while "0" in str(model_number):
            model_number += delta
        z = 0
        for digit, params in zip(str(model_number), PARAMS):
            z = get_next_z(int(digit), z, *params)
        if z == 0:
            break

    print(f"Part 2: {False}\n")


solve(actual_input)
