import os
import re

from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()

RACE_TIME = 2503

regex = re.compile(
    r"^(?P<reindeer>.+) can fly (?P<v>\d+) km/s for (?P<t>\d+) seconds, but then must rest for (?P<r>\d+) seconds\.$"
)


def distance(total_time, speed, flying_time, rest_time):
    flight_time = total_time // (flying_time + rest_time) * flying_time
    flight_time += min(flying_time, total_time % (flying_time + rest_time))
    return flight_time * speed


def solve(inputs):
    reindeer = {
        data["reindeer"]: (int(data["v"]), int(data["t"]), int(data["r"]))
        for data in (regex.match(line).groupdict() for line in inputs.splitlines())
    }
    print(f"Part 1: {max(distance(RACE_TIME, *r) for r in reindeer.values())}")

    scores = defaultdict(int)
    for t in range(1, RACE_TIME + 1):
        distances = defaultdict(list)
        for name, r in reindeer.items():
            distances[distance(t, *r)].append(name)
        for name in distances[max(distances.keys())]:
            scores[name] += 1
    print(f"Part 2: {max(scores.values())}\n")


solve(actual_input)