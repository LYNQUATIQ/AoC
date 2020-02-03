import logging
import os
import re

from collections import Counter


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_20.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_20_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Particle:
    def __init__(self, px, py, pz, vx, vy, vz, ax, ay, az):
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.ax = ax
        self.ay = ay
        self.az = az
        self.distance = abs(self.px) + abs(self.py) + abs(self.pz)

    def update_position(self):
        self.prior_distance = self.distance
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az
        self.px += self.vx
        self.py += self.vy
        self.pz += self.vz
        self.distance = abs(self.px) + abs(self.py) + abs(self.pz)

    @property
    def position(self):
        return (self.px, self.py, self.pz)

    @property
    def speeding_away(self):
        if self.ax * self.vx < 0 or self.ay * self.vy < 0 or self.az * self.vz < 0:
            return False
        if self.vx * self.px < 0 or self.vy * self.py < 0 or self.vz * self.pz < 0:
            return False
        return True


pattern = re.compile(
    r"^p=<(?P<px>-?\d+),(?P<py>-?\d+),(?P<pz>-?\d+)>, v=<(?P<vx>-?\d+),(?P<vy>-?\d+),(?P<vz>-?\d+)>, a=<(?P<ax>-?\d+),(?P<ay>-?\d+),(?P<az>-?\d+)>$"
)

particles = {}
for i, line in enumerate(lines):
    params = {k: int(v) for k, v in pattern.match(line).groupdict().items()}
    particles[i] = Particle(**params)

particles_in_play = set(particles.keys())
iterations = 0
while len(particles_in_play) > 1:
    for p in particles_in_play:
        particles[p].update_position()
    iterations += 1
    if iterations < 333:
        continue

    nearest_distance = None
    for p in particles_in_play:
        if nearest_distance is None or particles[p].distance < nearest_distance:
            nearest_distance = particles[p].distance

    take_out_of_play = set()
    for p in particles_in_play:
        if particles[p].distance > nearest_distance and particles[p].speeding_away:
            take_out_of_play.add(p)

    for p in take_out_of_play:
        particles_in_play.remove(p)

print(f"Part 1: {particles_in_play.pop()}")

particles = {}
for i, line in enumerate(lines):
    params = {k: int(v) for k, v in pattern.match(line).groupdict().items()}
    particles[i] = Particle(**params)

particles_in_play = set(particles.keys())
iterations = 0
while iterations < 1000:
    iterations += 1
    for p in particles_in_play:
        particles[p].update_position()

    position_counts = Counter([particles[p].position for p in particles_in_play])
    positions_to_remove = set([p for p, c in position_counts.items() if c > 1])
    take_out_of_play = set()
    for p in particles_in_play:
        if particles[p].position in positions_to_remove:
            take_out_of_play.add(p)

    for p in take_out_of_play:
        particles_in_play.remove(p)

print(f"Part 2: {len(particles_in_play)}")

