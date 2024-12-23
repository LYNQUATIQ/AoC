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


def bors_kerbosch(reported, potential, excluded, connections, maximal_clique):
    if not potential and not excluded:
        if len(reported) > len(maximal_clique):
            maximal_clique -= maximal_clique
            maximal_clique |= reported
        return

    for pc in set(potential):
        bors_kerbosch(
            reported | {pc},
            potential & connections[pc],
            excluded & connections[pc],
            connections,
            maximal_clique,
        )
        potential.remove(pc)
        excluded.add(pc)


@print_time_taken
def solve(inputs: str):

    connections = defaultdict(set)
    for line in inputs.splitlines():
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    connected_sets = set()
    for a, b, c in combinations(connections, 3):
        if not any(pc.startswith("t") for pc in (a, b, c)):
            continue
        if b in connections[a] and c in connections[a] and c in connections[b]:
            connected_sets.add(frozenset((a, b, c)))
    print(f"Part 1: {len(connected_sets)}")

    maximal_clique = set()
    bors_kerbosch(set(), set(connections), set(), connections, maximal_clique)
    print(f"Part 2:\n{','.join(sorted(maximal_clique))}\n")


solve(example_input)
solve(actual_input)
# at,gy,ih,ly,me,sm,tc,tj,tl,vf,vt,wn    is wrong
