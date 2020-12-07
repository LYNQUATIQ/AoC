import os
from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")

lines = [line.rstrip("\n") for line in open(input_file)]

asteroids = []
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "#":
            asteroids.append((x, y))


def get_los_vector(this, other):
    x1, y1 = this
    x2, y2 = other
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    direction = (round((x2 - x1) / distance, 5), round((y2 - y1) / distance, 5))
    return direction, distance


lines_of_sight = defaultdict(dict)
distances = defaultdict(dict)
in_sight = defaultdict(int)
for this_asteroid in asteroids:
    directions = set()
    for other_asteroid in asteroids:
        if other_asteroid == this_asteroid:
            continue
        direction, distance = get_los_vector(this_asteroid, other_asteroid)
        if direction in directions:
            if distance < distances[this_asteroid][direction]:
                lines_of_sight[this_asteroid][direction] = other_asteroid
                distances[this_asteroid][direction] = distance
        else:
            directions.add(direction)
            lines_of_sight[this_asteroid][direction] = other_asteroid
            distances[this_asteroid][direction] = distance
            in_sight[this_asteroid] += 1

numbers_in_sight = defaultdict(list)
for asteroid, number_in_sight in in_sight.items():
    numbers_in_sight[number_in_sight].append(asteroid)

asteroid + (22, 19)
