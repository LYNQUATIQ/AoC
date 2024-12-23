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
    for line in inputs.splitlines():
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)
    computers = set(connections)

    connected_sets = defaultdict(set)
    for a, b, c in combinations(connections, 3):
        if not any(pc.startswith("t") for pc in (a, b, c)):
            continue
        if b in connections[a] and c in connections[a] and c in connections[b]:
            connected_sets[3].add(frozenset((a, b, c)))
    print(f"Part 1: {len(connected_sets[3])}")

    to_visit = {(3, pc_set) for pc_set in connected_sets[3]}
    visited = set()
    while to_visit:
        set_size, pc_set = to_visit.pop()
        visited.add(pc_set)
        for pc in computers - pc_set:
            if all(pc in connections[x] for x in pc_set):
                new_pc_set = frozenset((*pc_set, pc))
                connected_sets[set_size + 1].add(new_pc_set)
                to_visit.add((set_size + 1, new_pc_set))

    lan_party = connected_sets[max(connected_sets)].pop()
    print(f"Part 2: {','.join(sorted(lan_party))}\n")


solve(example_input)
solve(actual_input)
# at,gy,ih,ly,me,sm,tc,tj,tl,vf,vt,wn    is wrong
