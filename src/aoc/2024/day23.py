"""https://adventofcode.com/2024/day/23"""

from collections import defaultdict
from itertools import combinations

from aoc_utils import get_input_data, print_time_taken

actual_input = get_input_data(2024, 23)
example_input = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


@print_time_taken
def solve(inputs: str):

    connections = defaultdict(set)
    lines = inputs.splitlines()
    for line in lines:
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    three_inter_connected = []
    for a, b, c in combinations(connections, 3):
        if not any(computer.startswith("t") for computer in (a, b, c)):
            continue
        if b in connections[a] and c in connections[a] and c in connections[b]:
            three_inter_connected.append((a, b, c))
    print(f"Part 1: {len(three_inter_connected)}")

    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
