from heapq import heappop, heappush
from typing import Any, Callable

from grid import Grid, XY

Node = Any
Neighbours = dict[Node, float]
Graph = dict[Node, Neighbours]


def calculate_distances(graph: Graph, starting_node: Node):
    distances = {node: float("inf") for node in graph}
    distances[starting_node] = 0
    to_visit: list[tuple[float, Node]] = [(0, starting_node)]
    while len(to_visit) > 0:
        current_distance, this_node = heappop(to_visit)
        if current_distance > distances[this_node]:
            continue
        for neighbour, distance in graph[this_node].items():
            distance += current_distance
            if distance < distances[neighbour]:
                distances[neighbour] = distance
                heappush(to_visit, (distance, neighbour))

    return distances


def a_star(
    grid: Grid,
    start: XY,
    target: XY,
    heuristic: Callable[[XY, XY], int] = lambda a, b: (a - b).manhattan_distance,
) -> list[XY] | None:

    visited: set[XY] = set()
    prior_step: dict[XY, XY] = {}

    g_scores = {start: 0}
    f_score = {start: heuristic(start, target)}

    to_visit: list[tuple[int, XY]] = []
    heappush(to_visit, (f_score[start], start))

    while to_visit:

        _, this_node = heappop(to_visit)

        if this_node == target:
            path = []
            while this_node in prior_step:
                path.append(this_node)
                this_node = prior_step[this_node]
            return path

        visited.add(this_node)
        for neighbour in grid.connected_nodes(this_node):
            tentative_g_score = g_scores[this_node] + 1
            actual_g_score = g_scores.get(neighbour, 0)

            if neighbour in visited and tentative_g_score >= actual_g_score:
                continue

            if tentative_g_score < actual_g_score or neighbour not in [
                i[1] for i in to_visit
            ]:
                prior_step[neighbour] = this_node
                g_scores[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + heuristic(neighbour, target)
                heappush(to_visit, (f_score[neighbour], neighbour))

    return None
