import logging
import os

import string

from collections import Counter
from itertools import permutations

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

# lines = ["1423", "121", "10290"]


def check_if_biggest(string):
    biggest = True
    i = 0
    while biggest and i < len(string):
        d = string[i]
        for c in string[i + 1 :]:
            if c > d:
                biggest = False
        i += 1
    return biggest


answer = 0
for line in lines:
    number = int(line)

    if check_if_biggest(line):
        print(f"{number} --> {number} (already biggest)")
        continue
    number_set = Counter(line)
    next_number = number + 1
    while Counter(str(next_number)) != number_set:
        next_number += 1
    print(f"{number} --> {next_number}")
    answer += next_number - number

print(answer)
