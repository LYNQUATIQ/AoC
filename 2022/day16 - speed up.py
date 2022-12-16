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

from heapq import heappop, heappush


from itertools import product

from collections import deque, namedtuple


State = namedtuple("State", "valve time_left flow to_open")


@print_time_taken
def max_release(inputs: str) -> int:
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

    def find_shortest_paths(start: str, targets: set[str]) -> dict[str, int]:
        queue = deque([start])
        distance_to = {start: 0}
        paths: dict[str, int] = {start: 0} if start in targets else {}
        while queue:
            valve = queue.popleft()
            if valve in targets and valve != start:
                paths[valve] = distance_to[valve] + 1  # Add 1 for opening
                if all(t in paths for t in targets):
                    if start in targets:
                        del paths[start]
                    return paths
            for next_valve in tunnels[valve]:
                if next_valve not in distance_to:
                    queue.append(next_valve)
                    distance_to[next_valve] = distance_to[valve] + 1
        raise ValueError("No path found")

    # Gather distances between target valves
    distances: dict[str, dict[str, int]] = {
        v: find_shortest_paths(v, valves_to_open) for v in valves_to_open
    }
    distances |= {"AA": find_shortest_paths("AA", valves_to_open)}

    # Do an a* search
    initial_state = State("AA", 30, 0, frozenset(valves_to_open))
    visited: set[State] = set()
    g_scores: dict[State, int] = {initial_state: 0}
    to_visit: list[tuple[int, State]] = []
    heappush(to_visit, (0, initial_state))
    while to_visit:
        _, this = heappop(to_visit)
        visited.add(this)
        to_open = frozenset(set(this.to_open) - {this.valve})

        next_moves = [
            (d, v) for v, d in distances[this.valve].items() if v in this.to_open
        ]
        for d, next_valve in next_moves:
            time_left = this.time_left - d
            if time_left < 0:
                continue
            flow = this.flow + flow_rates[next_valve]
            g_score = g_scores[this] + (d * this.flow)
            next_state = State(next_valve, time_left, flow, to_open)
            if next_state in visited and g_score <= g_scores.get(next_state, 0):
                continue
            else:
                g_scores[next_state] = g_score
                h_score = 0
                f_score = g_score + h_score
                heappush(to_visit, (-f_score, next_state))

    max_release = 0
    for state, g_score in g_scores.items():
        release = g_score + (state.time_left * state.flow)
        if release > max_release:
            max_release = release

    return max_release


def solve(inputs: str) -> None:
    print(f"Part 1: {max_release(inputs)}")
    # print(f"Part 2: {max_release(inputs, use_elephant=True)}\n")


solve(sample_input)
solve(actual_input)
