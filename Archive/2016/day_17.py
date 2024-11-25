import logging
import os

import hashlib

from collections import deque
from grid_system import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

passcode = "rrrbmfta"

directions = {
    "U": XY(0, -1),
    "D": XY(0, +1),
    "L": XY(-1, 0),
    "R": XY(+1, 0),
}


def connected_nodes(node, path_to_here):
    connected_nodes = {}
    hash_value = hashlib.md5(f"{passcode}{path_to_here}".encode()).hexdigest()
    for i, d in enumerate("UDLR"):
        if hash_value[i] in "bcdef":
            n = node + directions[d]
            if n.x in range(4) and n.y in range(4):
                connected_nodes[d] = n
    return connected_nodes


def bfs_path(start=XY(0, 0), goal=XY(3, 3), find_shortest=True):
    path_to_goal = None
    # Still need to visit (point, via path)
    to_visit = deque([(start, "")])
    while to_visit:
        this_node, path_so_far = to_visit.popleft()
        for d, next_node in connected_nodes(this_node, path_so_far).items():
            if next_node == goal:
                path_to_goal = path_so_far + d
                if find_shortest:
                    return path_to_goal
            else:
                to_visit.append((next_node, path_so_far + d))
    return path_to_goal


start = XY(0, 0)
goal = XY(3, 3)
print(f"Part 1: {bfs_path(start, goal)}")
print(f"Part 2: {len(bfs_path(start, goal, False))}")
