import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

orbits = dict(line.split(")")[::-1] for line in lines)


def get_orbit_path(planet):
    try:
        parent = orbits[planet]
    except KeyError:
        return []
    return [parent] + get_orbit_path(parent)


orbit_paths = {p: get_orbit_path(p) for p in orbits}

print(f"Part 1: {sum(len(x) for x in orbit_paths.values())}")

intersect = None
for p in orbit_paths["YOU"]:
    if p in orbit_paths["SAN"]:
        intersect = p
        break
part2 = orbit_paths["YOU"].index(intersect)
part2 += orbit_paths["SAN"].index(intersect)
print(f"Part 2: {part2}")
