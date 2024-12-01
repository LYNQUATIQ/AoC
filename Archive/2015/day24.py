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

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

packages = []
for line in lines:
    packages.append(int(line))


def qe(bucket):
    qe = 1
    for x in bucket:
        qe = qe * x
    return qe


def best_qe(n_compartments):
    target_weight = sum(packages) // n_compartments
    best_qe = None
    n_packages = 4
    while best_qe is None:
        for combo in combinations(packages, n_packages):
            if sum(combo) == target_weight:
                if best_qe is None or qe(combo) < best_qe:
                    best_qe = qe(combo)
        n_packages += 1

    return best_qe


print(f"Part 1: {best_qe(3)}")
print(f"Part 1: {best_qe(4)}")
