import logging
import os

import hashlib
import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

disk_initial = {
    1: 10,
    2: 15,
    3: 17,
    4: 1,
    5: 0,
    6: 1,
}

disks = {
    1: 13,
    2: 17,
    3: 19,
    4: 7,
    5: 5,
    6: 3,
}

t = 0
while True:
    if all([((t + d + disk_initial[d]) % disks[d]) == 0 for d in disks.keys()]):
        break
    t += 1

print(f"Part 1: {t}")

disk_initial[7] = 0
disks[7] = 11

t = 0
while True:
    if all([((t + d + disk_initial[d]) % disks[d]) == 0 for d in disks.keys()]):
        break
    t += 1

print(f"Part 2: {t}")
