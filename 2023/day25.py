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


def karger_min_cut(node_edges: dict[str, set[tuple[str, str]]]) -> tuple[int, int, int]:
    # Take a copy of the graoh and create counbters to keep track of nmerged nodes/edges
    graph, node_count, edge_count = {}, defaultdict(int), defaultdict(int)
    for node, connected_nodes in node_edges.items():
        graph[node] = set(connected_nodes)
        node_count[node] = 1
        for connected_node in connected_nodes:
            edge_count[frozenset([node, connected_node])] = 1

    while len(graph) > 2:
        target_node = random.choice(list(graph))
        node_to_merge = random.choice(list(graph[target_node]))
        node_count[target_node] += node_count[node_to_merge]
        graph[target_node].remove(node_to_merge)
        graph[node_to_merge].remove(target_node)
        for connected_node in (n for n in graph[node_to_merge] if n != target_node):
            graph[connected_node].remove(node_to_merge)
            graph[connected_node].add(target_node)
            graph[target_node].add(connected_node)
            old_edge = frozenset([node_to_merge, connected_node])
            new_edge = frozenset([target_node, connected_node])
            edge_count[new_edge] += edge_count[old_edge]
        del graph[node_to_merge]

    left_cluster, right_cluster = graph.keys()
    min_cut = frozenset([left_cluster, right_cluster])
    return edge_count[min_cut], node_count[left_cluster], node_count[right_cluster]


def solve(inputs: str):
    node_edges = defaultdict(set)
    for line in inputs.splitlines():
        this_node, connected_nodes = line.split(": ")
        for connected_node in connected_nodes.split():
            node_edges[this_node].add(connected_node)
            node_edges[connected_node].add(this_node)

    while True:
        min_cut, left_size, right_size = karger_min_cut(node_edges)
        if min_cut == 3:
            break

    print(f"Answer: {left_size * right_size }\n")


solve(sample_input)
solve(actual_input)
