import logging
import os
import sys

from itertools import groupby

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)


input_txt = "3113322113"

def look_and_say(digits):
    return "".join(str(len(list(l))) + d for d, l in groupby(digits))

digits = input_txt
for _ in range(40):
    digits = look_and_say(digits)
print(f"Part 1: {len(digits)}")

for _ in range(10):
    digits = look_and_say(digits)
print(f"Part 2: {len(digits)}")
