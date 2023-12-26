"""https://adventofcode.com/2023/day/25"""
import os
import random

from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day25_input.txt")) as f:
    actual_input = f.read()


sample_input = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


def apply_karger(node_edges: dict[str, set[tuple[str, str]]]) -> tuple[int, int, int]:
    # Take a copy of the graoh and counbters to keep track of nodes/edges merged
    graph, node_count, edge_count = {}, defaultdict(int), defaultdict(int)
    for node, edges in node_edges.items():
        graph[node] = set(edges)
        node_count[node] = 1
        for edge in edges:
            edge_count[tuple(sorted([node, edge]))] = 1

    while len(graph) > 2:
        node1 = random.choice(list(graph))
        node2 = random.choice(list(graph[node1]))
        node_count[node1] += node_count[node2]
        graph[node1].remove(node2)
        graph[node2].remove(node1)
        for other_node in graph[node2]:
            graph[other_node].remove(node2)
            graph[other_node].add(node1)
            graph[node1].add(other_node)
            old_edge = tuple(sorted([node2, other_node]))
            new_edge = tuple(sorted([node1, other_node]))
            edge_count[new_edge] += edge_count[old_edge]
            del edge_count[old_edge]
        del graph[node2]
        del node_count[node2]

    cluster1, cluster2 = graph.keys()
    edge = tuple(sorted([cluster1, cluster2]))
    return edge_count[edge], node_count[cluster1], node_count[cluster2]


def solve(inputs: str):
    node_edges = defaultdict(set)
    for line in inputs.splitlines():
        this_node, connected_nodes = line.split(": ")
        for connected_node in connected_nodes.split():
            node_edges[this_node].add(connected_node)
            node_edges[connected_node].add(this_node)

    while True:
        min_cut, cluster1_size, cluster2_size = apply_karger(node_edges)
        if min_cut == 3:
            break

    print(f"Answer: {cluster1_size* cluster2_size }\n")


solve(sample_input)
solve(actual_input)
