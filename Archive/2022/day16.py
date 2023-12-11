"""https://adventofcode.com/2022/day/16"""
import os
import re
from collections import deque
from heapq import heappop, heappush

from tqdm import tqdm

with open(os.path.join(os.path.dirname(__file__), "inputs/day16_input.txt")) as f:
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

#  State is a tuple time, valve, flow, targets
State = tuple[int, int, int, int]


def parse_inputs(
    inputs: str,
) -> tuple[dict[int, dict[int, int]], dict[int, int], int]:
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
    valve_distances: dict[str, dict[str, int]] = {
        v: find_shortest_paths(v, valves_to_open) for v in valves_to_open
    }
    valve_distances |= {"AA": find_shortest_paths("AA", valves_to_open)}

    flag_map: dict[str, int] = {v: 2**i for i, v in enumerate(valves_to_open)}
    flag_map["AA"] = 0
    target_valves = (2 ** len(valves_to_open)) - 1
    flows = {flag_map[v]: f for v, f in flow_rates.items() if f > 0}
    distances: dict[int, dict[int, int]] = {}
    for v, td in valve_distances.items():
        distances[flag_map[v]] = {flag_map[t]: d for t, d in td.items()}

    return distances, flows, target_valves


def max_release(
    distances: dict[int, dict[int, int]],
    flow_rates: dict[int, int],
    targets: int,
    max_time: int = 30,
) -> int:
    # Do an a* search
    initial_state = (0, 0, 0, targets)
    visited: set[State] = set()
    g_scores: dict[State, int] = {initial_state: 0}
    to_visit: list[tuple[int, State]] = []
    heappush(to_visit, (0, initial_state))
    while to_visit:
        _, state = heappop(to_visit)
        current_time, valve, current_flow, to_open = state
        visited.add(state)

        possible_moves = [(d, v) for v, d in distances[valve].items() if v & to_open]
        for steps, next_valve in possible_moves:
            if current_time + steps > max_time:
                continue

            next_time = current_time + steps
            next_flow = current_flow + flow_rates[next_valve]
            next_state = (
                next_time,
                next_valve,
                next_flow,
                to_open & ~next_valve,
            )
            g_score = g_scores[state] + (steps * current_flow)
            if next_state in visited and g_score <= g_scores.get(next_state, 0):
                continue
            else:
                g_scores[next_state] = g_score
                h_score = (max_time - next_time) * next_flow
                f_score = g_score + h_score
                heappush(to_visit, (-f_score, next_state))

    max_release = 0
    for (time, _, flow, _), g_score in g_scores.items():
        release = g_score + ((max_time - time) * flow)
        if release > max_release:
            max_release = release

    return max_release


def solve(inputs: str) -> None:
    distances, flow_rates, targets = parse_inputs(inputs)

    print(f"Part 1: {max_release(distances, flow_rates, targets, 30)}")

    maximum_release = 0
    for my_targets in tqdm(range(1, (targets + 1) // 2)):
        n_bits = bin(my_targets).count("1")
        if targets > 1000 and (n_bits <= 6 or n_bits >= 9):
            continue
        ele_targets = targets - my_targets
        my_flow = max_release(distances, flow_rates, my_targets, 26)
        ele_flow = max_release(distances, flow_rates, ele_targets, 26)
        maximum_release = max(maximum_release, my_flow + ele_flow)
    print(f"Part 2: {maximum_release}\n")


solve(sample_input)
solve(actual_input)
