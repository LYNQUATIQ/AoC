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

from collections import namedtuple


State = namedtuple(
    "State", "time_left flow to_open my_valve ele_valve my_last ele_last"
)


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

    visited: set[State] = set()
    initial_state = State(
        26 if use_elephant else 30, 0, frozenset(valves_to_open), "AA", "AA", "AA", "AA"
    )
    g_scores: dict[State, int] = {initial_state: 0}
    to_visit: list[tuple[int, State]] = []
    heappush(to_visit, (0, initial_state))
    while to_visit:
        _, s = heappop(to_visit)
        visited.add(s)

        time_left = s.time_left - 1
        if not time_left or not s.to_open:
            continue

        next_states = []
        my_moves = list(v for v in tunnels[s.my_valve] if v != s.my_last)
        if s.my_valve in s.to_open:
            my_moves.append(s.my_valve)
        if use_elephant:
            ele_moves = list(v for v in tunnels[s.ele_valve] if v != s.ele_last)
            if s.ele_valve in s.to_open and not s.my_valve == s.ele_valve:
                ele_moves.append(s.ele_valve)
        else:
            ele_moves = [s.ele_valve]

        for my_move, ele_move in product(my_moves, ele_moves):
            if (
                my_move == ele_move
                and (my_move != s.my_valve)
                and (ele_move != s.ele_valve)
            ):
                continue
            flow = s.flow
            to_open = set(s.to_open)
            if my_move == s.my_valve:
                flow += flow_rates[s.my_valve]
                to_open -= {s.my_valve}
            if use_elephant and ele_move == s.ele_valve:
                flow += flow_rates[s.ele_valve]
                to_open -= {s.ele_valve}
            next_states.append(
                State(
                    time_left,
                    flow,
                    frozenset(to_open),
                    my_move,
                    ele_move,
                    s.my_valve,
                    s.ele_valve,
                )
            )
        tentative_g = g_scores[s] + s.flow
        for next_state in next_states:
            actual_g = g_scores.get(next_state, 0)
            if next_state in visited and tentative_g <= actual_g:
                continue
            g_scores[next_state] = tentative_g
            potential_rate = s.flow
            if next_state.my_valve in s.to_open:
                potential_rate += flow_rates[next_state.my_valve]
            if next_state.ele_valve in s.to_open:
                potential_rate += flow_rates[next_state.ele_valve]
            h_score = potential_rate * time_left
            f_score = tentative_g + h_score
            heappush(to_visit, (-f_score, next_state))

    max_release = 0
    for s, g_score in g_scores.items():
        release = g_score + (s.time_left * s.flow)
        if release > max_release:
            max_release = release

    return max_release


def solve(inputs: str) -> None:
    print(f"Part 1: {max_release(inputs)}")
    print(f"Part 2: {max_release(inputs, use_elephant=True)}\n")


solve(sample_input)
solve(actual_input)
