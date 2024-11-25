import logging
import os

import re

from itertools import combinations

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="w",
)

row = 2981
column = 3075

count = sum(range(row)) + 1
delta = row + 1
for _ in range(1, column):
    count += delta
    delta += 1

initial_code = 20151125
multiplier = 252533
modulo = 33554393

code = initial_code
for _ in range(1, count):
    code = (code * multiplier) % modulo

print(f"Part 1: {code}")
