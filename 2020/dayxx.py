# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter
import itertools as it

from grid import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
# log_file = os.path.join(script_dir, f"logs/{script_name}.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """sample"""


def solve(inputs):
    # lines = inputs.split("\n")
    # values = [int(line) for line in inputs.split("\n")]

    print(f"Part 1: {False}")

    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
