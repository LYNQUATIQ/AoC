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
    clusters: dict[Cube, Cluster] = {}

    for x, y, z in cubes:
        nl, nr = (x - 1, y, z), (x + 1, y, z)
        nu, nd = (x, y - 1, z), (x, y + 1, z)
        nf, nb = (x, y, z - 1), (x, y, z + 1)
        linked_clusters = []
        for neighbour in (nl, nr, nu, nd, nf, nb):
            if neighbour not in cubes:
                sides += 1
            else:
                if neighbour in clusters:
                    if clusters[neighbour] not in linked_clusters:
                        linked_clusters.append(clusters[neighbour])

        if len(linked_clusters) == 0:
            this_cluster = Cluster()
        elif len(linked_clusters) == 1:
            (this_cluster,) = linked_clusters
        else:
            this_cluster = Cluster.combine_clusters(linked_clusters)
            for cluster in linked_clusters:
                for xyz in cluster.cubes:
                    clusters[xyz] = this_cluster
        clusters[(x, y, z)] = this_cluster
        this_cluster.add((x, y, z))
    print(f"Part 1: {sides}")

    gaps = set()
    extent = max(*(max(cube) for cube in cubes)) + 1

    for x0, y0, z0 in product(range(extent), range(extent), range(extent)):
        if (x0, y0, z0) in cubes:
            continue
        l = next(
            ((x, y0, z0) for x in range(x0 - 1, -1, -1) if (x, y0, z0) in cubes), None
        )
        r = next(
            ((x, y0, z0) for x in range(x0 + 1, extent) if (x, y0, z0) in cubes), None
        )
        u = next(
            ((x0, y, z0) for y in range(y0 - 1, -1, -1) if (x0, y, z0) in cubes), None
        )
        d = next(
            ((x0, y, z0) for y in range(y0 + 1, extent) if (x0, y, z0) in cubes), None
        )
        f = next(
            ((x0, y0, z) for z in range(z0 - 1, -1, -1) if (x0, y0, z) in cubes), None
        )
        b = next(
            ((x0, y0, z) for z in range(z0 + 1, extent) if (x0, y0, z) in cubes), None
        )
        if all((l, r, u, d, f, b)):
            if len(set(id(clusters[xyz]) for xyz in (l, r, u, d, f, b))) == 1:
                gaps.add((x0, y0, z0))
            if all(distance((x0, y0, z0), xyz) == 1 for xyz in (l, r, u, d, f, b)):
                gaps.add((x0, y0, z0))

    for x, y, z in gaps:
        sides -= (x - 1, y, z) in cubes
        sides -= (x + 1, y, z) in cubes
        sides -= (x, y - 1, z) in cubes
        sides -= (x, y + 1, z) in cubes
        sides -= (x, y, z - 1) in cubes
        sides -= (x, y, z + 1) in cubes

    print(f"Part 2: {sides}\n")
    print(len(set(clusters.values())))


# Incorrect 2602, 2634
# 2958 too high

solve(sample_input)
solve(actual_input)
