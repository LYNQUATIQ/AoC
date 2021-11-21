# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter
from itertools import product

from grid import XY, ConnectedGrid
from utils import *

# log_file = os.path.join(os.path.dirname(__file__), f"logs/dayxx.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
with open(os.path.join(os.path.dirname(__file__), f"inputs/dayxx_input.txt")) as f:
    actual_input = f.read()

sample_input = """sample"""


@print_time_taken
def solve(inputs):
    # lines = inputs.splitlines()
    # values = list(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")

    print(f"Part 2: {False}\n")


solve(sample_input)
# solve(actual_input)
