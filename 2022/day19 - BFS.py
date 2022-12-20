"""https://adventofcode.com/2022/day/19"""
import os
import re

from utils import print_time_taken
from tqdm import tqdm

with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()


sample_input = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

REGEX = r"^Blueprint (?P<i>\d+): Each ore robot costs (?P<o1>\d+) ore. Each clay robot costs (?P<o2>\d+) ore. Each obsidian robot costs (?P<o3>\d+) ore and (?P<cl>\d+) clay. Each geode robot costs (?P<o4>\d+) ore and (?P<ob>\d+) obsidian.$"

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
NONE = -1
# ELEMENTS = (GEODE, OBSIDIAN, CLAY, ORE)  # ...in this order to improve heuristic
ELEMENTS = (ORE, CLAY, OBSIDIAN, GEODE)

MAX_TIME = 24

# Blueprint is a tuple of ore costs, and the clay and obsidian requirments
BluePrint = tuple[tuple[int, int, int, int], int, int]

# State is a tuple of time, initial bots, initial resources and which bot to build
State = tuple[int, tuple[int, ...], tuple[int, ...], int]

from collections import deque
from heapq import heappop, heappush


@print_time_taken
def max_geodes(blueprint: BluePrint) -> int:
    ore_costs, clay_cost, obsidian_cost = blueprint
    initial_bots = (1, 0, 0, 0)
    initial_state = (1, (0, 0, 0, 0), initial_bots, NONE)

    prior_states: dict[State, State] = {}
    g_scores: dict[State, int] = {initial_state: 0}

    # heappush(to_visit, (0, initial_state))
    queue = deque([initial_state])
    while queue:
        state = queue.popleft()
        time, resources, bots, bot_to_build = state

        if time == MAX_TIME:
            continue

        # Collect resources that existing bots generate
        next_resources = list(resources[e] + bots[e] for e in ELEMENTS)

        # Spend resources to build new bots
        next_bots = list(bots)
        if bot_to_build != NONE:
            next_bots[bot_to_build] += 1
            next_resources[ORE] -= ore_costs[bot_to_build]
            if bot_to_build == OBSIDIAN:
                next_resources[CLAY] -= clay_cost
            if bot_to_build == GEODE:
                next_resources[OBSIDIAN] -= obsidian_cost

        # if next_resources[ORE] > max(ore_costs):  # Make sure we're spending enough?????
        #     continue

        # Determine what bots we should build next
        ore, clay, obsidian, _ = next_resources
        add_do_nothing = False

        bot_options = []
        if ore >= ore_costs[GEODE] and obsidian >= obsidian_cost:
            bot_options = [GEODE]
        else:
            add_do_nothing |= (ore + bots[GEODE]) >= ore_costs[GEODE]
            if ore >= ore_costs[OBSIDIAN] and clay >= clay_cost:
                bot_options = [OBSIDIAN]
            else:
                add_do_nothing |= (ore + bots[OBSIDIAN]) >= ore_costs[OBSIDIAN]
                if ore >= ore_costs[CLAY]:
                    bot_options = [CLAY]
                else:
                    add_do_nothing |= (ore + bots[CLAY]) >= ore_costs[CLAY]
                    if ore >= ore_costs[ORE]:
                        bot_options = [ORE]
                    add_do_nothing = True
        if add_do_nothing:
            bot_options.append(NONE)

        for bot_to_build in bot_options:
            next_state = (
                time + 1,
                tuple(next_resources),
                tuple(next_bots),
                bot_to_build,
            )

            if next_state in g_scores:
                continue
            g_scores[next_state] = next_resources[GEODE] + next_bots[GEODE]
            queue.append(next_state)
            prior_states[next_state] = state

    max_geodes = max(g_scores.values())
    return max_geodes

    max_states = [s for s, g in g_scores.items() if s[0] == 24 and g == max_geodes]
    path = [max_states[0]]
    s = path[0]
    while True:
        try:
            s = prior_states[s]
        except KeyError:
            break
        path.append(s)
    elem = {ORE: "ore", CLAY: "clay", OBSIDIAN: "obsidian", GEODE: "geode"}
    for time, resources, bots, bot_to_build in sorted(path):
        print(f"\n== Minute {time} ==")
        res = list(resources)
        if bot_to_build != NONE:
            res[ORE] -= ore_costs[bot_to_build]
            extra = ""
            if bot_to_build == GEODE:
                extra = f" and {obsidian_cost} obsidian"
                res[OBSIDIAN] -= obsidian_cost
            if bot_to_build == OBSIDIAN:
                extra = f" and {clay_cost} clay"
                res[CLAY] -= clay_cost
            print(
                f"Spend {ore_costs[bot_to_build]} ore{extra} to start building a {elem[bot_to_build]} robot."
            )
        for i in ELEMENTS:

            if bots[i] > 0:
                e = elem[i]
                print(
                    f"{bots[i]} {e} robot collect {bots[i]} {e}; you now have {res[i] + bots[i]} {e}."
                )
        if bot_to_build != NONE:
            print(
                f"The new {elem[bot_to_build]} robot is ready; you now have {bots[bot_to_build] +1} of them."
            )

    return max_geodes


@print_time_taken
def solve(inputs: str) -> None:
    blueprints: dict[int, BluePrint] = {}
    for bp in inputs.splitlines():
        match = re.match(REGEX, bp)
        assert match is not None
        bp_id, ore1, ore2, ore3, ore4, clay_cost, obsidian_cost = (
            int(match.groupdict()[x]) for x in ("i", "o1", "o2", "o3", "o4", "cl", "ob")
        )
        blueprints[bp_id] = ((ore1, ore2, ore3, ore4), clay_cost, obsidian_cost)
        # print(bp_id, ore4 + obsidian_cost * ore3 + obsidian_cost * clay_cost * ore2)

    part1 = 0

    for bp_id, blueprint in tqdm(blueprints.items()):
        max_g = max_geodes(blueprint)
        part1 += bp_id * max_g
        print(f"{bp_id}: {max_g}\n")

    # case = 19
    # print(f"{case}: {max_geodes(blueprints[case])}\n")

    print(f"Part 1: {part1}")
    # print(f"Part 2: {False}\n")


# Part 1 - 954 too low, 1077 WRONG

# solve(sample_input)
solve(actual_input)
