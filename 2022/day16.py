"""https://adventofcode.com/2022/day/16"""
import os
import re
from collections import deque, namedtuple
from heapq import heappop, heappush
from itertools import combinations

from tqdm import tqdm

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


State = namedtuple("State", "time valve flow to_open")


def parse_inputs(
    inputs: str,
) -> tuple[dict[str, dict[str, int]], dict[str, int], set[str]]:
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
                paths[valve] = distance_to[valve] + 1  # +1 for opening valve
                if all(t in paths for t in targets):
                    if start in targets:
                        del paths[start]
                    return paths
            for next_valve in tunnels[valve]:
                if next_valve not in distance_to:
                    queue.append(next_valve)
                    distance_to[next_valve] = distance_to[valve] + 1
        raise ValueError("No path found")

    # Calculate steps between target valves (plus the steps from the start)
    distances: dict[str, dict[str, int]] = {
        v: find_shortest_paths(v, valves_to_open) for v in valves_to_open
    }
    distances |= {"AA": find_shortest_paths("AA", valves_to_open)}

    return distances, flow_rates, valves_to_open


def max_release(
    distances: dict[str, dict[str, int]],
    flow_rates: dict[str, int],
    targets: set[str],
    max_time: int = 30,
) -> int:

    # Do an a* search
    initial_state = State(0, "AA", 0, frozenset(targets))
    visited: set[State] = set()
    g_scores: dict[State, int] = {initial_state: 0}
    to_visit: list[tuple[int, State]] = []
    heappush(to_visit, (0, initial_state))
    while to_visit:
        _, this = heappop(to_visit)
        visited.add(this)

        options = this.to_open - {this.valve}
        if not options:
            continue
        possible_moves = [
            (d, v) for v, d in distances[this.valve].items() if v in options
        ]

        for (steps, next_valve) in possible_moves:
            if this.time + steps > max_time:
                continue

            flow, to_open = this.flow, set(this.to_open)
            flow += flow_rates[next_valve]
            to_open -= {next_valve}

            next_state = State(
                this.time + steps,
                next_valve,
                flow,
                frozenset(to_open),
            )
            g_score = g_scores[this] + (steps * this.flow)
            if next_state in visited and g_score <= g_scores.get(next_state, 0):
                continue
            else:
                g_scores[next_state] = g_score
                h_score = (max_time - next_state.time) * next_state.flow
                f_score = g_score + h_score
                heappush(to_visit, (-f_score, next_state))

    max_release = 0
    for state, g_score in g_scores.items():
        release = g_score + ((max_time - state.time) * state.flow)
        if release > max_release:
            max_release = release

    return max_release


def partition_set(items: set[str]):
    results = set()
    for l in range(0, int(len(items) / 2) + 1):
        combis = set(combinations(items, l))
        for c in combis:
            if len(c) > len(items) // 3:
                results.add((frozenset(list(c)), frozenset(list(items - set(c)))))
    drop_list = set()
    for a, b in results:
        if (b, a) in results and (a, b) not in drop_list:
            drop_list.add((b, a))
    for d in drop_list:
        results.discard(d)
    return results


def solve(inputs: str) -> None:

    distances, flow_rates, targets = parse_inputs(inputs)

    print(f"Part 1: {max_release(distances, flow_rates, targets, 30)}")

    maximum_release = 0
    for my_target, ele_targets in tqdm(partition_set(targets)):
        my_flow = max_release(distances, flow_rates, my_target, 26)
        ele_flow = max_release(distances, flow_rates, ele_targets, 26)
        maximum_release = max(maximum_release, my_flow + ele_flow)
    print(f"Part 2: {maximum_release}\n")


solve(sample_input)
solve(actual_input)
