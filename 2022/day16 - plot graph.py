"""https://adventofcode.com/2022/day/16"""
import os
import re
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day16_input.txt")) as f:
    actual_input = f.read()


sample_input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

REGEX = r"^Valve (?P<valve>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<tunnels>.+)$"

import plotly.graph_objects as go

import networkx as nx
import matplotlib.pyplot as plt


def solve(inputs: str) -> None:
    flow_rates: dict[str, int] = {}
    tunnels: dict[str, tuple[str, ...]] = {}
    valves_to_open: set[str] = set()
    for line in inputs.splitlines():
        match = re.match(REGEX, line)
        assert match is not None
        valve = match["valve"]
        flow_rates[valve] = int(match["rate"])
        tunnels[valve] = tuple(match["tunnels"].split(", "))
        if flow_rates[valve] > 0:
            valves_to_open.add(valve)

    edges = []
    for v, ns in tunnels.items():
        for n in ns:
            edges.append((v, n))
    G = nx.Graph()
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap("jet"), node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)
    plt.show()


# solve(sample_input)
solve(actual_input)
