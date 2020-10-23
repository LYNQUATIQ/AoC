import logging
import os

import string

from collections import Counter


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

bad_pairs = ["ab", "cd", "pq", "xy"]
double_pairs = [c * 2 for c in string.ascii_lowercase]

nice_words = 0
for word in lines:
    counts = Counter(word)
    if sum(counts.get(v, 0) for v in "aeiou") < 3:
        continue
    if not any((pair in word for pair in double_pairs)):
        continue
    if any((pair in word for pair in bad_pairs)):
        continue
    nice_words += 1

print(f"Part 1: {nice_words}")


nice_words = 0
for word in lines:
    found_two_pair = False
    for i in range(len(word) - 3):
        if word.find(word[i : i + 2], i + 2) != -1:
            found_two_pair = True
            break
    if not found_two_pair:
        continue
    found_aba = False
    for i, c in enumerate(word[:-2]):
        if word[i + 2] == c:
            found_aba = True
            continue
    if not found_aba:
        continue
    nice_words += 1

print(f"Part 2: {nice_words}")
