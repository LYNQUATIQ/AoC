import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_24.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_24_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


components = set()
starting_components = set()
links = defaultdict(list)

for line in lines:
    a, b = (int(i) for i in line.split("/"))
    if a < b:
        component = (a, b)
    else:
        component = (b, a)
    components.add(component)
    links[a].append(component)
    links[b].append(component)
    if min(a, b) == 0:
        starting_components.add(component)


def build_bridges(current_bridge=[], current_port=0):
    available_components = [c for c in components if c not in current_bridge]
    possible_components = [c for c in links[current_port] if c in available_components]
    if not possible_components:
        return [current_bridge]

    bridges = []
    for component in possible_components:
        port_a, port_b = component
        if port_a == current_port:
            next_port = port_b
        else:
            next_port = port_a
        bridges += build_bridges(current_bridge + [component], next_port)

    return bridges


def bridge_strength(bridge):
    return sum(a + b for a, b in bridge)


bridges = build_bridges()

max_strength = 0
longest_bridges = []
longest_length = 0
for bridge in bridges:
    max_strength = max(max_strength, bridge_strength(bridge))
    bridge_length = len(bridge)
    if bridge_length > longest_length:
        longest_length = bridge_length
        longest_bridges = [bridge]
    elif bridge_length == longest_length:
        longest_bridges.append(bridge)

print(f"Part 1: {max_strength}")

max_strength = 0
for bridge in longest_bridges:
    max_strength = max(max_strength, bridge_strength(bridge))

print(f"Part 2: {max_strength}")
