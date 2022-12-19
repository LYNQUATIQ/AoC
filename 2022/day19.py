"""https://adventofcode.com/2022/day/19"""
import os
import re

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


def max_geodes(blueprint: BluePrint) -> int:
    ore_costs, clay_cost, obsidian_cost = blueprint
    initial_bots = (1, 0, 0, 0)
    initial_state = (1, (0, 0, 0, 0), initial_bots, NONE)

    prior_states: dict[State, State] = {}
    best_geo_bots_at_t: dict[int, int] = {}
    g_scores: dict[State, int] = {initial_state: 0}
    visited: set[State] = set()
    to_visit: list[tuple[float, State]] = []

    heappush(to_visit, (0, initial_state))

    while to_visit:
        _, state = heappop(to_visit)
        visited.add(state)
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

        # Make sure we're spending enough
        if next_resources[ORE] > max(ore_costs):
            continue

        # Determine what bots we can build next
        ore, clay, obsidian, _ = next_resources
        bot_options: set[int] = {NONE}
        if ore >= ore_costs[ORE]:
            bot_options.add(ORE)
        if ore >= ore_costs[CLAY] and not clay > clay_cost * 3:
            bot_options.add(CLAY)
        if (
            ore >= ore_costs[OBSIDIAN]
            and clay >= clay_cost
            and not obsidian > obsidian_cost * 3
        ):
            bot_options.add(OBSIDIAN)
        if ore >= ore_costs[GEODE] and obsidian >= obsidian_cost:
            bot_options = {GEODE}  # If we can build a geode bot then *just* do that!
            # bot_options.add(GEODE)

        for bot_to_build in sorted(bot_options, reverse=True):
            next_state = (
                time + 1,
                tuple(next_resources),
                tuple(next_bots),
                bot_to_build,
            )
            if best_geo_bots_at_t.get(time, 0) > next_resources[GEODE]:
                continue

            g_score = next_resources[GEODE] + next_bots[GEODE]
            if next_state in visited and g_score <= g_scores.get(next_state, 0):
                continue
            g_scores[next_state] = g_score
            h_score = next_bots[GEODE] * (MAX_TIME - time)
            f_score = g_score + 0  # h_score
            heappush(to_visit, (-f_score, next_state))
            prior_states[next_state] = state
            best_geo_bots_at_t[time + 1] = next_resources[GEODE]

    max_geodes = max(g_scores.values())
    # states = [state]
    # s = state
    # while True:
    #     try:
    #         s = prior_states[s]
    #     except KeyError:
    #         break
    #     states.append(s)
    # elem = {ORE: "ore", CLAY: "clay", OBSIDIAN: "obsidian", GEODE: "geode"}
    # for time, resources, bots, bot_to_build in sorted(states):
    #     print(f"\n== Minute {time} ==")
    #     res = list(resources)
    #     if bot_to_build != NONE:
    #         res[ORE] -= ore_costs[bot_to_build]
    #         extra = ""
    #         if bot_to_build == GEODE:
    #             extra = f" and {obsidian_cost} obsidian"
    #             res[OBSIDIAN] -= obsidian_cost
    #         if bot_to_build == OBSIDIAN:
    #             extra = f" and {clay_cost} clay"
    #             res[CLAY] -= clay_cost
    #         print(
    #             f"Spend {ore_costs[bot_to_build]} ore{extra} to start building a {elem[bot_to_build]} robot."
    #         )
    #     for i in ELEMENTS:

    #         if bots[i] > 0:
    #             e = elem[i]
    #             print(
    #                 f"{bots[i]} {e} robot collect {bots[i]} {e}; you now have {res[i] + bots[i]} {e}."
    #             )
    #     if bot_to_build != NONE:
    #         print(
    #             f"The new {elem[bot_to_build]} robot is ready; you now have {bots[bot_to_build] +1} of them."
    #         )

    return max_geodes


from utils import print_time_taken


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

    part1 = sum(
        bp_id * max_geodes(blueprint) for bp_id, blueprint in blueprints.items()
    )
    print(f"Part 1: {part1}")
    # print(f"Part 2: {False}\n")


# Part 1 - 954 too low

solve(sample_input)
solve(actual_input)
