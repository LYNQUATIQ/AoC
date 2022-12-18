"""https://adventofcode.com/2022/day/18"""
from __future__ import annotations

import os
import re

from itertools import product
from typing import Iterable

with open(os.path.join(os.path.dirname(__file__), f"inputs/day18_input.txt")) as f:
    actual_input = f.read()


sample_input = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

Cube = tuple[int, int, int]


class Cluster:
    def __init__(self, cubes: set[Cube] | None = None) -> None:
        cubes = cubes or set()
        self._cubes: set[Cube] = cubes

    @property
    def cubes(self) -> set[Cube]:
        return self._cubes

    def add(self, cube: Cube) -> None:
        self._cubes.add(cube)

    @classmethod
    def combine_clusters(cls, clusters: Iterable[Cluster]) -> Cluster:
        all_cubes = [c for cluster in clusters for c in cluster.cubes]
        return Cluster(set(all_cubes))


distance = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def solve(inputs: str) -> None:
    cubes = set(tuple(map(int, re.findall(r"\d+", l))) for l in inputs.splitlines())

    sides = 0
    for x, y, z in cubes:
        nl, nr = (x - 1, y, z), (x + 1, y, z)
        nu, nd = (x, y - 1, z), (x, y + 1, z)
        nf, nb = (x, y, z - 1), (x, y, z + 1)
        for neighbour in (nl, nr, nu, nd, nf, nb):
            sides += neighbour not in cubes
    print(f"Part 1: {sides}")

    extent = max(*(max(cube) for cube in cubes)) + 1
    gaps = set()
    for x, y, z in product(range(extent), range(extent), range(extent)):
        if (x, y, z) in cubes:
            continue
        gaps.add((x, y, z))

    gap_clusters: dict[Cube, Cluster] = {}
    for x, y, z in gaps:
        nl, nr = (x - 1, y, z), (x + 1, y, z)
        nu, nd = (x, y - 1, z), (x, y + 1, z)
        nf, nb = (x, y, z - 1), (x, y, z + 1)
        linked_clusters = []
        for neighbour in (nl, nr, nu, nd, nf, nb):
            if neighbour in gap_clusters:
                if gap_clusters[neighbour] not in linked_clusters:
                    linked_clusters.append(gap_clusters[neighbour])
        if len(linked_clusters) == 0:
            this_cluster = Cluster()
        elif len(linked_clusters) == 1:
            (this_cluster,) = linked_clusters
        else:
            this_cluster = Cluster.combine_clusters(linked_clusters)
            for cluster in linked_clusters:
                for xyz in cluster.cubes:
                    gap_clusters[xyz] = this_cluster
        gap_clusters[(x, y, z)] = this_cluster
        this_cluster.add((x, y, z))

    open_air = gap_clusters[(0, 0, 0)]
    for space in open_air.cubes:
        gaps.discard(space)

    for x, y, z in gaps:
        sides -= (x - 1, y, z) in cubes
        sides -= (x + 1, y, z) in cubes
        sides -= (x, y - 1, z) in cubes
        sides -= (x, y + 1, z) in cubes
        sides -= (x, y, z - 1) in cubes
        sides -= (x, y, z + 1) in cubes

    print(f"Part 2: {sides}\n")


solve(sample_input)
solve(actual_input)
