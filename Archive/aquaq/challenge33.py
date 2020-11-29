import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


target = 245701
MAX_DARTS = target // 60 + 5

finishes = defaultdict(set)

one_dart_finishes = set((25, 50))
for i in range(1, 21):
    one_dart_finishes.add(i)
    one_dart_finishes.add(i * 2)
    one_dart_finishes.add(i * 3)

n_dart_finishes = one_dart_finishes.copy()

all_finishes = {i: 1 for i in one_dart_finishes}
for darts in range(1, MAX_DARTS):
    n_plus_one_dart_finishes = set()
    for dn in n_dart_finishes:
        for d1 in one_dart_finishes:
            if (dn + d1) not in all_finishes:
                n_plus_one_dart_finishes.add(dn + d1)
    for i in n_plus_one_dart_finishes:
        all_finishes[i] = darts + 1
    n_dart_finishes = n_plus_one_dart_finishes

total_darts = 0
for t in range(1, target + 1):
    total_darts += all_finishes[t]

print(total_darts)
