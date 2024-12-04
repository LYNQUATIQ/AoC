"""https://adventofcode.com/2018/day/23"""

from __future__ import annotations
import os
import re

from itertools import product

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day23_input.txt")) as f:
    actual_input = f.read()


example_input = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""


from typing import NamedTuple


class XYZ(NamedTuple("XYZ", [("x", int), ("y", int), ("z", int)])):
    def __new__(cls, *_tuple):
        return tuple.__new__(cls, _tuple)

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return type(self)(self.x * scalar, self.y * scalar, self.z * scalar)

    def manhattan_distance(self, other=None):
        other = other if other else XYZ(0, 0, 0)
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class Nanobot:
    def __init__(self, x, y, z, radius):
        self.xyz = XYZ(x, y, z)
        self.radius = radius

    def in_range(self, xyz: XYZ):
        return self.xyz.manhattan_distance(xyz) <= self.radius


class NanobotCloud:
    def __init__(self, inputs):
        self.min_x, self.max_x = 0, 0
        self.min_y, self.max_y = 0, 0
        self.min_z, self.max_z = 0, 0

        self.bots = []
        for line in inputs.splitlines():
            x, y, z, radius = list(map(int, re.findall(r"-?\d+", line)))
            self.min_x, self.max_x = min(self.min_x, x), max(self.max_x, x)
            self.min_y, self.max_y = min(self.min_y, y), max(self.max_y, y)
            self.min_z, self.max_z = min(self.min_z, z), max(self.max_z, z)
            self.bots.append(Nanobot(x, y, z, radius))

    def strongest_bot(self):
        strongest_bot = self.bots[0]
        for bot in self.bots:
            if bot.radius > strongest_bot.radius:
                strongest_bot = bot
        return strongest_bot

    def bots_in_range(self, xyz):
        return sum(bot.in_range(xyz) for bot in self.bots)

    def local_maxima(self, seed_xyz, radius):
        directions = list(
            XYZ(*d) for d in product((-1, 0, 1), repeat=3) if d != (0, 0, 0)
        )
        best_xyz, max_bots = seed_xyz, self.bots_in_range(seed_xyz)
        for d in directions:
            xyz = seed_xyz + (d * radius)
            n = self.bots_in_range(xyz)
            if n > max_bots or (
                n == max_bots
                and xyz.manhattan_distance() < best_xyz.manhattan_distance()
            ):
                best_xyz, max_bots = xyz, n
        return best_xyz

    def brute_force(self, seed_xyz, radius):
        best_xyz = seed_xyz
        max_bots = self.bots_in_range(seed_xyz)
        for x in range(seed_xyz.x - radius, seed_xyz.x + radius):
            for y in range(seed_xyz.y - radius, seed_xyz.y + radius):
                for z in range(seed_xyz.z - radius, seed_xyz.z + radius):
                    xyz = XYZ(x, y, z)
                    n = self.bots_in_range(xyz)
                    if n > max_bots or (
                        n == max_bots
                        and xyz.manhattan_distance() < best_xyz.manhattan_distance()
                    ):
                        max_bots = n
                        best_xyz = xyz
        return best_xyz


@print_time_taken
def solve(inputs):
    cloud = NanobotCloud(inputs)
    strongest_bot = cloud.strongest_bot()
    print(f"Part 1: {sum(strongest_bot.in_range(other.xyz) for other in cloud.bots)}")

    xyz = XYZ(
        cloud.min_x + (cloud.max_x - cloud.min_x) // 2,
        cloud.min_y + (cloud.max_y - cloud.min_y) // 2,
        cloud.min_z + (cloud.max_z - cloud.min_z) // 2,
    )
    radius = 2**32
    while radius >= 1:
        last_xyz = None
        while xyz != last_xyz:
            last_xyz = xyz
            xyz = cloud.local_maxima(xyz, radius)
        radius = radius // 2
    print(f"Part 2: {cloud.brute_force(xyz, 8).manhattan_distance()}")


solve(example_input)
solve(actual_input)
