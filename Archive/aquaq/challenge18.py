import logging
import os

import datetime

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

times = []
for line in lines:
    hh, mm, ss = map(int, line.split(":"))
    times.append(datetime.time(hh, mm, ss))

palindromic_times = set()
for i in range(236):
    h1 = i // 100
    h2 = i % 100 // 10
    m1 = i % 10
    m2 = m1
    s1 = h2
    s2 = h1
    h = h1 * 10 + h2
    m = m1 * 10 + m2
    s = s1 * 10 + s2
    try:
        palindromic_times.add(datetime.time(h, m, s))
    except ValueError:
        pass


def time_diff(t1, t2):
    a = datetime.datetime.combine(datetime.date.min, t1)
    b = datetime.datetime.combine(datetime.date.min, t2)
    d = abs(a - b).total_seconds()
    if d > 12 * 60 * 60:
        d = 24 * 60 * 60 - d
    return int(d)


answer = 0
for t in times:
    min_p = None
    min_s = 24 * 60 * 60
    for p in palindromic_times:
        d = time_diff(t, p)
        if d < min_s:
            min_s = d
            min_p = p
    print(f"{t} -> {min_p}   {min_s}s")
    answer += min_s

print(answer)
