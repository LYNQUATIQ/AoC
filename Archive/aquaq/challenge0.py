import logging
import os

import bisect
from collections import Counter

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

numpad = {
    0: {1: " "},
    2: {1: "a", 2: "b", 3: "c"},
    3: {1: "d", 2: "e", 3: "f"},
    4: {1: "g", 2: "h", 3: "i"},
    5: {1: "j", 2: "k", 3: "l"},
    6: {1: "m", 2: "n", 3: "o"},
    7: {1: "p", 2: "q", 3: "r", 4: "s"},
    8: {1: "t", 2: "u", 3: "v"},
    9: {1: "w", 2: "x", 3: "y", 4: "z"},
}

output = ""
for line in lines:
    a, b = line[0], line[2]
    output += numpad[int(a)][int(b)]

print(output)
