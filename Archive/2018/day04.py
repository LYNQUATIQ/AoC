"""https://adventofcode.com/2018/day/4"""
import os
import re

from collections import defaultdict, deque

with open(os.path.join(os.path.dirname(__file__), "inputs/day04_input.txt")) as f:
    actual_input = f.read()

sample_input = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

REGEX = (
    r"^\[(?P<yyyymmdd>\d{4}-\d{2}-\d{2}) (?P<hh>\d{2}):(?P<mm>\d{2})\] (?P<comment>.+)$"
)
GUARD_REGX = r"^Guard #(?P<guard>\d+) begins shift$"


def solve(inputs):
    comments = []
    for line in inputs.splitlines():
        match = re.match(REGEX, line)
        comments.append((match["yyyymmdd"], match["hh"], match["mm"], match["comment"]))
    observations = deque(sorted(comments))

    guards = defaultdict(lambda: defaultdict(int))
    while observations:
        _, _, start, comment = observations.popleft()
        if match := re.match(GUARD_REGX, comment):
            guard = int(match.groupdict()["guard"])
            continue
        _, _, end, comment = observations.popleft()
        for minute in range(int(start), int(end)):
            guards[guard][minute] += 1
    total_asleep = {k: sum(v.values()) for k, v in guards.items()}

    guard = max(total_asleep, key=total_asleep.get)
    print(f"Part 1: {guard * max(guards[guard], key=guards[guard].get)}")

    guard = max(guards, key=lambda x: max(guards[x].values()))
    print(f"Part 2: {guard * max(guards[guard], key=guards[guard].get)}\n")


solve(sample_input)
solve(actual_input)
