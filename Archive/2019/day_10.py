import math
import os
from collections import defaultdict

from grid_system import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")


def angle(x):
    RADIANS = 2 * math.pi
    return (math.atan2(*x) - RADIANS) % RADIANS


lines = [line.rstrip("\n") for line in open(input_file)]
asteroids = []
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "#":
            asteroids.append(XY(x, y))


lines_of_sight = defaultdict(lambda: defaultdict(list))
best_asteroid = None
for this_asteroid in asteroids:
    for other_asteroid in asteroids:
        if other_asteroid == this_asteroid:
            continue
        xd = other_asteroid.x - this_asteroid.x
        yd = this_asteroid.y - other_asteroid.y
        distance = abs(math.gcd(xd, yd))
        direction = (xd // distance, yd // distance)
        lines_of_sight[this_asteroid][direction].append((distance, other_asteroid))

best_asteroid = max(lines_of_sight, key=lambda x: len(lines_of_sight.get(x)))
print(f"Part 1: {len(lines_of_sight[best_asteroid])}")


los = sorted(list(lines_of_sight[best_asteroid].keys()), key=angle)
part2 = (sorted(lines_of_sight[best_asteroid][los[199]])[0])[1]
print(f"Part 2: {part2[0]:02}{part2[1]:02}")
