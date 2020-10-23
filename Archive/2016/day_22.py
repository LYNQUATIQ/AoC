import logging
import os
import re

from collections import defaultdict, deque, Counter
from itertools import permutations
from typing import NamedTuple

from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

regex = re.compile(r"\/dev\/grid\/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<available>\d+)T\s+\d+%$")
nodes = {}


class Node:
    
    def __init__(self, x, y, size, used, available):
        self.xy = XY(x, y)
        self.size = size
        self.used = used
        self.available = available

    def __repr__(self):
        return f"{self.xy} [{self.used:3}/{self.size:3}]"

    def adjust_load(self, amount):
        self.used += amount
        self.available -= amount
        assert (self.used <= self.size)


def reset_nodes(lines):
    for line in lines:
        node_dict = {k:int(v) for k,v in regex.match(line).groupdict().items()}
        new_node = Node(**node_dict)
        try:
            node = nodes[new_node.xy]
            node.size = new_node.size
            node.used = new_node.used
            node.available = new_node.available
        except KeyError:
            node = Node(**node_dict)
        nodes[node.xy] = node

def print_array(limit_y=999):
    max_x, max_y = 32, 28
    max_y = min(max_y, limit_y)
    header1 = "     " + "".join([" " * 9 + str(x+1) for x in range(max_x//10)])
    header2 = "    " + "".join([str(x % 10) for x in range(max_x)])
    print(header1); print(header2)
    for y in range(max_y):
        print(f"{y:3d} ", end="")
        for x in range(max_x):
            n = nodes[XY(x, y)]
            if n == target_node:
                s = "T"
            elif n.used > 100:
                s = u"\u2588"
            elif n.used > 1:
                s = "#"
            else:
                s = " "
            print(s, end="")
        print(f" {y:<3d} ")
    print(header2); print(header1)

def viable_pair(a, b):
    return a.used != 0 and a.used <= b.available

def move_node(a, b):
    if not viable_pair(a, b):
        print(f"ERROR - can't move {a} to {b}")
        raise Exception
    b.adjust_load(a.used)
    a.adjust_load(-a.used)


reset_nodes(lines)

viable_pairs = [(a, b) for a, b in permutations(nodes.values(), 2) if viable_pair(a, b)]
print(f"Part 1: {len(viable_pairs)}")

blank_node = nodes[XY(24, 22)]
target_node = nodes[XY(31, 0)]
steps = "L" * 16
steps += "U" * 22
steps += "R" * 23
steps += "DLLUR" * 30
print_array()
for s in steps:
    direction = {"L": XY(-1, 0), "U": XY(0, -1), "R": XY(1, 0), "D": XY(0, 1), }[s]
    node = nodes[blank_node.xy + direction]
    move_node(node, blank_node)
    if node == target_node:
        target_node = blank_node
    blank_node = node
print_array()

print(f"Part 2: {len(steps)}")