"""https://adventofcode.com/2024/day/23"""

from collections import defaultdict

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

    def bors_kerbosch(clique, potential, excluded, part_1_cliques, part_2_clique):
        if len(clique) == 3 and any(pc.startswith("t") for pc in clique):
            part_1_cliques.add(frozenset(clique))
        if not potential and not excluded:
            if len(clique) > len(part_2_clique):
                part_2_clique -= part_2_clique
                part_2_clique |= clique
            return
        for pc in set(potential):
            bors_kerbosch(
                clique | {pc},
                potential & connections[pc],
                excluded & connections[pc],
                part_1_cliques,
                part_2_clique,
            )
            potential.remove(pc)
            excluded.add(pc)

    part_1_cliques, part_2_clique = set(), set()
    bors_kerbosch(set(), set(connections), set(), part_1_cliques, part_2_clique)
    print(f"Part 1: {len(part_1_cliques)}")
    print(f"Part 2: {','.join(sorted(part_2_clique))}\n")


solve(example_input)
solve(actual_input)
