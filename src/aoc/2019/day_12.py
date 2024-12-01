import math
import os
import re

from collections import defaultdict
from itertools import combinations

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Moon:
    def __init__(self, x, y, z):
        self.position = (x, y, z)
        self.velocity = (0, 0, 0)

    def __repr__(self):
        return f"<pos={self.position} vel={self.velocity}>"

    def apply_velocity(self):
        x, y, z = self.position
        dx, dy, dz = self.velocity
        self.position = (x + dx, y + dy, z + dz)

    def apply_gravity(self, dx, dy, dz):
        x, y, z = self.velocity
        self.velocity = (x + dx, y + dy, z + dz)

    def pe(self):
        return sum(abs(c) for c in self.position)

    def ke(self):
        return sum(abs(c) for c in self.velocity)

    def total_energy(self):
        return self.pe() * self.ke()


moons = {}
for i, line in enumerate(lines):
    xyz = re.match(r"^<x=([-]?\d+), y=([-]?\d+), z=([-]?\d+)>$", line).groups()
    moons[i] = Moon(*(int(c) for c in xyz))

t = 0
while t < 1000:
    for i, j in combinations(moons, 2):
        m1, m2 = moons[i], moons[j]
        x1, y1, z1 = m1.position
        x2, y2, z2 = m2.position
        dx = (x1 < x2) - (x1 > x2)
        dy = (y1 < y2) - (y1 > y2)
        dz = (z1 < z2) - (z1 > z2)
        m1.apply_gravity(dx, dy, dz)
        m2.apply_gravity(-dx, -dy, -dz)
    for m in moons.values():
        m.apply_velocity()
    t += 1

print(f"Part 1: {sum(m.total_energy() for m in moons.values())}")


def x_period(positions):
    velocity = [0] * len(positions)
    original_positions = positions.copy()
    original_velocity = velocity.copy()
    pairs = list(combinations(range(len(positions)), 2))
    t = 0
    while True:
        t += 1
        for i, j in pairs:
            x1, x2 = positions[i], positions[j]
            dx = (x1 < x2) - (x1 > x2)
            velocity[i] += dx
            velocity[j] -= dx
        positions = [p + v for p, v in zip(positions, velocity)]
        if velocity == original_velocity and positions == original_positions:
            break
    return t


positions = defaultdict(list)
for i, line in enumerate(lines):
    xyz = re.match(r"^<x=([-]?\d+), y=([-]?\d+), z=([-]?\d+)>$", line).groups()
    positions["x"].append(int(xyz[0]))
    positions["y"].append(int(xyz[1]))
    positions["z"].append(int(xyz[2]))


def lcm(values):
    lcm = values[0]
    for i in values[1:]:
        lcm = lcm * i // math.gcd(lcm, i)
    return lcm


print(f"Part 2: {lcm(list(x_period(p) for p in positions.values()))}")
