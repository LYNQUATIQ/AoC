"""https://adventofcode.com/2022/day/16"""
import os
import re

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

REGEX = r"^Valve (?P<valve>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<neighbours>.+)$"

from heapq import heappop, heappush

from collections import deque
from itertools import permutations


def solve(inputs: str) -> None:
    rates: dict[str, int] = {}
    neighbours: dict[str, list[str]] = {}
    target_valves = set()
    for line in inputs.splitlines():
        match = re.match(REGEX, line)
        assert match is not None
        valve = match["valve"]
        rates[valve] = int(match["rate"])
        neighbours[valve] = list(match["neighbours"].split(", "))
        if rates[valve] > 0:
            target_valves.add(valve)

    def find_shortest_paths(start: str, targets: set[str]) -> dict[str, int]:
        print("Getting routes from ", start)
        queue = deque([start])
        distance_to = {start: 0}
        paths: dict[str, int] = {start: 0} if start in targets else {}
        while queue:
            valve = queue.popleft()
            if valve in targets and valve != start:
                paths[valve] = distance_to[valve]
                if all(t in paths for t in targets):
                    return paths
            for next_valve in neighbours[valve]:
                if next_valve not in distance_to:
                    queue.append(next_valve)
                    distance_to[next_valve] = distance_to[valve] + 1
        raise ValueError("No path found")

    distances = {"AA": find_shortest_paths("AA", target_valves)}
    distances |= {v: find_shortest_paths(v, target_valves) for v in target_valves}

    print(distances)
    max_release = 0
    for route in permutations(target_valves):
        route = ["AA"] + list(route)
        time, release = 0, 0
        current = 0
        for this_valve, next_valve in zip(route[:-1], route[1:]):
            time += distances[this_valve][next_valve]
            time += 1
            current += rates[next_valve]
            # print(
            #     f"At time {time} open valve {next_valve} - current flow now {current}"
            # )
            if time >= 30:
                break
            release += (30 - time) * rates[next_valve]
        max_release = max(max_release, release)

    print(f"Part 1: {max_release}")
    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
