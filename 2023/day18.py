"""https://adventofcode.com/2023/day/18"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day18_input.txt")) as f:
    actual_input = f.read()


sample_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

DIRECTIONS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


def solve(inputs: str):
    xy = (0, 0)
    lagoon_edges = {xy: ""}
    for line in inputs.splitlines():
        direction, steps, color = line.split()
        for _ in range(int(steps)):
            lagoon_edges[xy] = color[1:-1]
            dx, dy = DIRECTIONS[direction]
            xy = (xy[0] + dx, xy[1] + dy)
    min_x = min(xy[0] for xy in lagoon_edges)
    max_x = max(xy[0] for xy in lagoon_edges)
    min_y = min(xy[1] for xy in lagoon_edges)
    max_y = max(xy[1] for xy in lagoon_edges)

    lagoon = set()
    to_visit = {(1, 1)}
    while to_visit:
        xy = to_visit.pop()
        lagoon.add(xy)
        for dx, dy in DIRECTIONS.values():
            next_xy = (xy[0] + dx, xy[1] + dy)
            if next_xy in lagoon or next_xy in lagoon_edges:
                continue
            to_visit.add(next_xy)

    if False:
        for y in range(min_y - 1, max_y + 2):
            line = ""
            for x in range(min_x - 1, max_x + 2):
                assert not ((x, y) in lagoon_edges and (x, y) in lagoon)
                xy = (x, y)
                c = "."
                if xy in lagoon_edges:
                    c = "#"
                if xy in lagoon:
                    c = "~"
                line += c
            print(line)
        print()

    print(f"Part 1: {len(lagoon_edges)+len(lagoon)}")
    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
# 49321 - WRONG
