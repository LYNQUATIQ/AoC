import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

race_time = 2503

reindeer = {}
for line in lines:
    tokens = line.split(" ")
    reindeer[tokens[0]] = (int(tokens[3]), int(tokens[6]), int(tokens[13]))

def distance(total_time, speed, flying_time, rest_time):
    flight_time = total_time // (flying_time + rest_time) * flying_time
    flight_time += min(flying_time, total_time % (flying_time + rest_time))
    return flight_time * speed

print(f"Part 1: {max(distance(race_time, *r) for r in reindeer.values())}")

scores = defaultdict(int)
for t in range(1, race_time + 1):
    distances = defaultdict(list)
    for name, r in reindeer.items():
        distances[distance(t, *r)].append(name)
    for name in distances[max(distances.keys())]:
        scores[name] += 1

print(f"Part 2: {max(scores.values())}")

    

