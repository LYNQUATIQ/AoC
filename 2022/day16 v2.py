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

# State records the current time, the valve that a and b are moving towards or opening,
# the time that a and b will be ready to move, the flow rate as of now, and the set of
# valves still needing opening as of now
State = namedtuple("State", "time a_valve b_valve a_ready b_ready flow to_open")


@print_time_taken
def max_release(inputs: str, use_elephant=False) -> int:
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

    # Do an a* search
    max_time = 26 if use_elephant else 30
    initial_state = State(0, "AA", "AA", 0, 0, 0, frozenset(valves_to_open))
    visited: set[State] = set()
    g_scores: dict[State, int] = {initial_state: 0}
    to_visit: list[tuple[int, State]] = []
    heappush(to_visit, (0, initial_state))
    # paths: dict[State, list[State]] = {initial_state: []}
    while to_visit:
        _, this = heappop(to_visit)
        visited.add(this)
        # if this == State(
        #     time=9,
        #     a_valve="CC",
        #     b_valve="EE",
        #     a_ready=9,
        #     b_ready=11,
        #     flow=78,
        #     to_open=frozenset({"EE"}),
        # ):
        #     breakpoint()

        a_moving, b_moving = (this.a_ready == this.time, this.b_ready == this.time)
        options = this.to_open - {this.a_valve} - {this.b_valve}
        if a_moving:
            if options:
                a_moves = [
                    (d, v) for v, d in distances[this.a_valve].items() if v in options
                ]
            else:
                a_moves = [(99, this.a_valve)]
        else:
            a_moves = [(this.a_ready - this.time, this.a_valve)]
        if use_elephant:
            if b_moving:
                if options:
                    b_moves = [
                        (d, v)
                        for v, d in distances[this.b_valve].items()
                        if v in options
                    ]
                else:
                    b_moves = [(99, this.b_valve)]
            else:
                b_moves = [(this.b_ready - this.time, this.b_valve)]
        else:
            b_moves = [(99, "AA")]

        for (a_steps, a_next), (b_steps, b_next) in product(a_moves, b_moves):
            if a_next == b_next:  # Don't go to the same place
                continue
            steps = min(a_steps, b_steps)
            if this.time + steps > max_time:
                continue

            flow, to_open = this.flow, set(this.to_open)
            if steps == a_steps:
                flow += flow_rates[a_next]
                to_open -= {a_next}
            if steps == b_steps:
                flow += flow_rates[b_next]
                to_open -= {b_next}

            next_state = State(
                this.time + steps,
                a_next,
                b_next,
                this.time + a_steps,
                this.time + b_steps,
                flow,
                frozenset(to_open),
            )
            g_score = g_scores[this] + (steps * this.flow)
            if next_state in visited and g_score <= g_scores.get(next_state, 0):
                continue
            else:
                g_scores[next_state] = g_score
                h_score = 0
                f_score = g_score + h_score
                heappush(to_visit, (-f_score, next_state))
                # paths[next_state] = paths[this] + [this]

    max_release = 0
    # best_state = None
    for state, g_score in g_scores.items():
        release = g_score + ((max_time - state.time) * state.flow)
        if release > max_release:
            max_release = release
    #         best_state = state
    # assert best_state is not None
    # for p in list(paths[best_state]) + [best_state]:

    #     print(
    #         f"{p.time:2d}: ",
    #         p.a_valve if not p.a_valve in p.to_open else "  ",
    #         p.b_valve if not p.b_valve in p.to_open else "  ",
    #         f" {p.flow:2d} ",
    #         ",".join(v for v in valves_to_open if v in p.to_open),
    #     )

    return max_release


def solve(inputs: str) -> None:
    print(f"Part 1: {max_release(inputs)}")
    print(f"Part 2: {max_release(inputs, use_elephant=True)}\n")


solve(sample_input)
solve(actual_input)
