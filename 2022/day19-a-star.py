"""https://adventofcode.com/2022/day/19"""
import math
import os
import re

from heapq import heappop, heappush

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()


sample_input = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

REGEX = r"^Blueprint (?P<i>\d+): Each ore robot costs (?P<o1>\d+) ore. Each clay robot costs (?P<o2>\d+) ore. Each obsidian robot costs (?P<o3>\d+) ore and (?P<cl>\d+) clay. Each geode robot costs (?P<o4>\d+) ore and (?P<ob>\d+) obsidian.$"

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
DO_NOTHING = -1
# ELEMENTS = (GEODE, OBSIDIAN, CLAY, ORE)  # ...in this order to improve heuristic
ELEMENTS = (ORE, CLAY, OBSIDIAN, GEODE)


# Blueprint is a tuple of ore costs, and the clay and obsidian requirments
BluePrint = tuple[tuple[int, int, int, int], int, int]

# State is a tuple of time, initial bots, initial resources and which bot to build
State = tuple[int, tuple[int, ...], tuple[int, ...], int]

from collections import deque


def print_path(blueprint, g_scores, prior_states) -> None:
    ore_costs, clay_cost, obsidian_cost = blueprint

    max_geodes = max(g_scores.values())
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
    for time, resources, bots, bot_to_build in sorted(path):  # type: ignore
        print(f"\n== Minute {time} ==")
        res = list(resources)
        if bot_to_build != DO_NOTHING:
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
        if bot_to_build != DO_NOTHING:
            print(
                f"The new {elem[bot_to_build]} robot is ready; you now have {bots[bot_to_build] +1} of them."
            )


@print_time_taken
def find_max_geodes(blueprint: BluePrint, max_minutes: int, debug: bool = False) -> int:
    ore_costs, clay_cost, obsidian_cost = blueprint
    initial_bots = (1, 0, 0, 0)
    initial_state = (1, (0, 0, 0, 0), initial_bots, DO_NOTHING)

    prior_states: dict[State, State] = {}
    g_scores: dict[State, int] = {initial_state: 0}
    visited: set[State] = set()
    to_visit: list[tuple[float, State]] = []

    heappush(to_visit, (0, initial_state))
    while to_visit:
        f_score, state = heappop(to_visit)
        print(f_score, state, len(to_visit))
        visited.add(state)
        time, resources, bots, bot_to_build = state

        if time == max_minutes:
            break

        # Collect resources that existing bots generate
        next_resources = list(resources[e] + bots[e] for e in ELEMENTS)

        # Spend resources to build new bots
        next_bots = list(bots)
        if bot_to_build != DO_NOTHING:
            next_bots[bot_to_build] += 1
            next_resources[ORE] -= ore_costs[bot_to_build]
            if bot_to_build == OBSIDIAN:
                next_resources[CLAY] -= clay_cost
            if bot_to_build == GEODE:
                next_resources[OBSIDIAN] -= obsidian_cost

        # Determine what bots we should build next
        ore, clay, obsidian, _ = next_resources
        need_ore = bots[ORE] < max(ore_costs)
        need_clay = bots[CLAY] < clay_cost
        need_obsidian = bots[OBSIDIAN] < obsidian_cost
        can_make_ore = ore >= ore_costs[ORE]
        can_make_clay = ore >= ore_costs[CLAY]
        can_make_obsidian = ore >= ore_costs[OBSIDIAN] and clay >= clay_cost
        can_make_geode = ore >= ore_costs[GEODE] and obsidian >= obsidian_cost

        if can_make_geode:
            bot_options = {GEODE}
        else:
            if need_obsidian and can_make_obsidian:
                bot_options = {OBSIDIAN, DO_NOTHING}
            else:
                bot_options = {DO_NOTHING}
                if need_clay and can_make_clay:
                    bot_options.add(CLAY)
                if need_ore and can_make_ore:
                    bot_options.add(ORE)

        for bot_to_build in bot_options:
            next_state = (
                time + 1,
                tuple(next_resources),
                tuple(next_bots),
                bot_to_build,
            )

            g_score = next_resources[GEODE] + next_bots[GEODE]
            if next_state in visited and g_score <= g_scores.get(next_state, 0):
                continue
            g_scores[next_state] = g_score
            h_score = calc_h_score(next_state, max_minutes, obsidian_cost * clay_cost)
            f_score = g_score + h_score
            heappush(to_visit, (-f_score, next_state))
            prior_states[next_state] = state

    if debug:
        print_path(blueprint, g_scores, prior_states)

    return max(g_scores.values())


def calc_h_score(state: State, max_time: int, obs_x_clay_cost: int) -> float:
    time, resources, bots, bot_to_build = state

    geode_bots = bots[GEODE] + (1 if bot_to_build == GEODE else 0)
    obs_bots = bots[OBSIDIAN] + (1 if bot_to_build == OBSIDIAN else 0)
    clay_bots = bots[CLAY] + (1 if bot_to_build == CLAY else 0)
    _, clay, obsidian, _ = resources
    time_remaining = max_time - time
    multiplier = 0.5 * time_remaining * (time_remaining + 1)

    h = (multiplier ** 3) * (time_remaining + clay_bots)
    h += (multiplier ** 2) * (clay + obs_bots)
    h += multiplier * obsidian
    h /= obs_x_clay_cost
    h += multiplier * geode_bots

    return h


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

    quality_levels = []
    for bp_id, blueprint in blueprints.items():
        max_geode = find_max_geodes(blueprint, 24)
        quality_levels.append(bp_id * max_geode)
        print(f"{bp_id}:  {max_geode} geodes")
    print(f"Part 1: {sum(quality_levels)}")

    # first_3_blueprints = list(blueprints.values())[:3]
    # max_geodes = [find_max_geodes(blueprint, 32) for blueprint in first_3_blueprints]
    # print(f"Part 2: {max_geodes}\n")
    # print(f"Part 2: {math.prod(max_geodes)}\n")


# solve(sample_input)
solve(actual_input)
