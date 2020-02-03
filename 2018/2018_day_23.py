import logging
import os
import re

from typing import NamedTuple


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_23.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, f"inputs/2018_day_23_input.txt")
lines = [line.rstrip("\n") for line in open(file_path)]

pattern = re.compile(
    r"^pos=<(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)>, r=(?P<radius>\d+)$"
)


class XYZ:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"x:{self.x}, y:{self.y}, z:{self.z}"

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return type(self)(self.x * scalar, self.y * scalar, self.z * scalar)

    def distance(self, other=None):
        if other is None:
            other = XYZ(0, 0, 0)
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def within_area(self, bottom_xyz, top_xyz):
        return all(
            [
                self.x >= bottom_xyz.x,
                self.x < top_xyz.x,
                self.y >= bottom_xyz.y,
                self.y < top_xyz.y,
                self.z >= bottom_xyz.z,
                self.z < top_xyz.z,
            ]
        )


class Nanobot(XYZ):
    def __init__(self, x, y, z, radius):
        super().__init__(x, y, z)
        self.radius = radius

    def __repr__(self):
        return f"x:{self.x}, y:{self.y}, z:{self.z} - radius:{self.radius}"

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def in_range(self, other):
        return self.distance(other) <= self.radius


class NanobotCloud:
    def __init__(self, lines):
        self.min_x, self.max_x = 0, 0
        self.min_y, self.max_y = 0, 0
        self.min_z, self.max_z = 0, 0

        self.nanobots = []
        for line in lines:
            regex = pattern.match(line).groupdict()
            x, y, z, radius = (
                int(regex["x"]),
                int(regex["y"]),
                int(regex["z"]),
                int(regex["radius"]),
            )
            self.nanobots.append(Nanobot(x, y, z, radius))
            self.min_x = min(self.min_x, x)
            self.min_y = min(self.min_y, y)
            self.min_z = min(self.min_z, z)
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)
            self.max_z = max(self.max_z, z)
        # print(self.min_x, self.max_x, self.max_x - self.min_x)
        # print(self.min_y, self.max_y, self.max_y - self.min_y)
        # print(self.min_z, self.max_z, self.max_z - self.min_z)

    def strongest_nanobot(self):
        strongest_nanobot = self.nanobots[0]
        for nanobot in self.nanobots:
            if nanobot.radius > strongest_nanobot.radius:
                strongest_nanobot = nanobot
        return strongest_nanobot

    def nanonbots_within_range_of_nanobot(self, this_nanobot):
        i = 0
        for nanobot in self.nanobots:
            if this_nanobot.in_range(nanobot):
                i += 1
        return i

    def nanobots_in_range(self, xyz):
        i = 0
        for nanobot in self.nanobots:
            if nanobot.in_range(xyz):
                i += 1
        return i

    def show_density(self):
        x_step = (self.max_x - self.min_x) // 5 + 1
        y_step = (self.max_y - self.min_y) // 5 + 1
        z_step = (self.max_z - self.min_z) // 5 + 1
        for xi, x in enumerate(range(self.min_x, self.max_x + 1, x_step)):
            for yi, y in enumerate(range(self.min_y, self.max_y + 1, y_step)):
                for zi, z in enumerate(range(self.min_z, self.max_z + 1, z_step)):
                    i = 0
                    bottom_xyz = XYZ(x, y, z)
                    top_xyz = XYZ(x + x_step, y + y_step, z + z_step)
                    for n in self.nanobots:
                        if n.within_area(bottom_xyz, top_xyz):
                            i += 1
                    # print(f"Block {xi}{yi}{zi} - {i} nanobots")
                    print(
                        f"Block {xi}{yi}{zi} - {bottom_xyz} - {self.nanobots_in_range(bottom_xyz)} in range"
                    )

    def local_maxima(self, seed_xyz, radius):
        directions = [
            XYZ(-1, -1, -1),
            XYZ(-1, -1, 0),
            XYZ(-1, -1, 1),
            XYZ(-1, 0, -1),
            XYZ(-1, 0, 0),
            XYZ(-1, 0, 1),
            XYZ(-1, 1, -1),
            XYZ(-1, 1, 0),
            XYZ(-1, 1, 1),
            XYZ(0, -1, -1),
            XYZ(0, -1, 0),
            XYZ(0, -1, 1),
            XYZ(0, 0, -1),
            XYZ(0, 0, 0),
            XYZ(0, 0, 1),
            XYZ(0, 1, -1),
            XYZ(0, 1, 0),
            XYZ(0, 1, 1),
            XYZ(1, -1, -1),
            XYZ(1, -1, 0),
            XYZ(1, -1, 1),
            XYZ(1, 0, -1),
            XYZ(1, 0, 0),
            XYZ(1, 0, 1),
            XYZ(1, 1, -1),
            XYZ(1, 1, 0),
            XYZ(1, 1, 1),
        ]
        best_xyz = seed_xyz
        max_nanobots = self.nanobots_in_range(seed_xyz)
        for d in directions:
            xyz = seed_xyz + (d * radius)
            n = self.nanobots_in_range(xyz)
            if n > max_nanobots or (
                n == max_nanobots and xyz.distance() < best_xyz.distance()
            ):
                max_nanobots = n
                best_xyz = xyz
        return best_xyz, max_nanobots

    def brute_force(self, seed_xyz, radius):
        best_xyz = seed_xyz
        max_nanobots = self.nanobots_in_range(seed_xyz)
        for x in range(seed_xyz.x - radius, seed_xyz.x + radius):
            for y in range(seed_xyz.y - radius, seed_xyz.y + radius):
                for z in range(seed_xyz.z - radius, seed_xyz.z + radius):
                    xyz = XYZ(x, y, z)
                    n = self.nanobots_in_range(xyz)
                    if n > max_nanobots or (
                        n == max_nanobots and xyz.distance() < best_xyz.distance()
                    ):
                        max_nanobots = n
                        best_xyz = xyz
        return best_xyz, max_nanobots


nanobot_cloud = NanobotCloud(lines)
strongest_nanobot = nanobot_cloud.strongest_nanobot()
print(f"Part 1: {nanobot_cloud.nanonbots_within_range_of_nanobot(strongest_nanobot)}")

xyz = XYZ(24821516, 63351834, 77647984)
xyz = XYZ(0, 0, 0)
xyz = XYZ(10000000, 20000000, 30000000)
radius = 2 ** 30
while radius >= 1:
    last_xyz = None
    while xyz != last_xyz:
        last_xyz = xyz
        xyz, nanobots_in_range = nanobot_cloud.local_maxima(xyz, radius)
        print(
            f"xyz: {xyz}   Radius: {radius}   Nanobots: {nanobots_in_range}/{len(nanobot_cloud.nanobots)}"
        )
    radius = radius // 2

xyz, nanobots_in_range = nanobot_cloud.brute_force(xyz, 8)
print(f"xyz: {xyz}   Nanobots: {nanobots_in_range}/{len(nanobot_cloud.nanobots)}")
print(f"Part 2: {xyz.distance()}")

