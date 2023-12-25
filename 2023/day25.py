"""https://adventofcode.com/2023/day/25"""
import os

from collections import defaultdict, deque

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


def solve(inputs: str):
    node_edges = defaultdict(set)
    for line in inputs.splitlines():
        this_node, connected_nodes = line.split(": ")
        for connected_node in connected_nodes.split():
            node_edges[this_node].add(connected_node)
            node_edges[connected_node].add(this_node)

    # Calculate how many times each edge is traversed when travelling between all nodes
    traversal_count = defaultdict(int)
    for node in node_edges:
        visited = set([node])
        to_visit = deque([(node, [])])
        while to_visit:
            for _ in range(len(to_visit)):
                this_node, path = to_visit.popleft()
                for edge in path:
                    traversal_count[edge] += 1
                for next_node in node_edges[this_node]:
                    if next_node not in visited:
                        visited.add(next_node)
                        edge = tuple(sorted((next_node, this_node)))
                        to_visit.append((next_node, path + [edge]))

    # Remove three most frequently traversed edges
    most_traversed = sorted(traversal_count, key=traversal_count.get, reverse=True)
    for left, right in most_traversed[:3]:
        node_edges[left].remove(right)
        node_edges[right].remove(left)

    # Find size of any one of the clusters
    visited = set([node])
    to_visit = [node]
    while to_visit:
        this_node = to_visit.pop()
        for next_node in node_edges[this_node]:
            if next_node not in visited:
                visited.add(next_node)
                to_visit.append(next_node)

    print(f"Answer: {len(visited) * (len(node_edges)-len(visited)) }\n")


solve(sample_input)
solve(actual_input)
