# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter
import itertools as it

from grid import XY, ConnectedGrid
from utils import *

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
# log_file = os.path.join(script_dir, f"logs/{script_name}.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """0,3,6"""
actual_input = """18,11,9,0,5,1"""


def solve(inputs):
    numbers = [int(line) for line in inputs.split(",")]

    turn = 0
    when_said = defaultdict(list)
    prior_spoken = {}
    last_spoken = {}
    last_number_said = None
    for number in numbers:
        turn += 1
        last_number_said = number
        when_said[last_number_said].append(turn)

    while True:
        times_spoken = when_said[last_number_said]
        try:
            last_number_said = turn - times_spoken[-2]
        except IndexError:
            last_number_said = 0
        turn += 1
        when_said[last_number_said].append(turn)
        # print(f"Turn {turn}: {last_number_said}")
        if turn == 2020:
            print(f"Part 1: {last_number_said}")
            break
        if turn == 30000000:
            break

    # for k in sorted(when_said.keys()):
    #     print(k, when_said[k])
    print(f"Part 2: {last_number_said}\n")


solve(sample_input)
solve(actual_input)
