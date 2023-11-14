"""https://adventofcode.com/2022/day/19"""
from math import ceil, prod
import os
import re

from contextlib import redirect_stdout

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
ELEMENTS = (ORE, CLAY, OBSIDIAN, GEODE)


# Blueprint is a tuple of ore costs, and the clay and obsidian requirments
BluePrint = tuple[tuple[int, int, int, int], int, int]

# State is a tuple of time, initial bots, initial resources and which bot to build
State = tuple[int, tuple[int, ...], tuple[int, ...], int]

from collections import deque

SAMPLE_ANSWERS = {
    24: {1: 9, 2: 12},
    32: {1: 56, 2: 62},
}
ACTUAL_ANSWERS = {
    1: 0,
    2: 0,
    3: 1,
    4: 5,
    5: 3,
    6: 2,
    7: 0,
    8: 1,
    9: 14,
    10: 0,
    11: 1,
    12: 0,
    13: 5,
    14: 6,
    15: 0,
    16: 0,
    17: 1,
    18: 0,
    19: 15,
    20: 6,
    21: 0,
    22: 5,
    23: 0,
    24: 0,
    25: 6,
    26: 4,
    27: 1,
    28: 0,
    29: 8,
    30: 0,
}


def print_path(blueprint, g_scores, prior_states, max_time) -> None:
    ore_costs, obsidianbot_clay_cost, geobot_obsidian_cost = blueprint

    max_geodes = max(g_scores.values())
    max_states = [
        s for s, g in g_scores.items() if s[0] == max_time and g == max_geodes
    ]
    path = [max_states[0]]
    s = path[0]
    while True:
        try:
            s = prior_states[s]
        except KeyError:
            break
        path.append(s)
    elem = {ORE: "ore", CLAY: "clay", OBSIDIAN: "obsidian", GEODE: "geode"}
    for state in sorted(path):  # type: ignore
        time, resources, bots, bot_to_build = state
        print(f"\n== Minute {time} ==", state)
        res = list(resources)
        if bot_to_build != DO_NOTHING:
            res[ORE] -= ore_costs[bot_to_build]
            extra = ""
            if bot_to_build == GEODE:
                extra = f" and {geobot_obsidian_cost} obsidian"
                res[OBSIDIAN] -= geobot_obsidian_cost
            if bot_to_build == OBSIDIAN:
                extra = f" and {obsidianbot_clay_cost} clay"
                res[CLAY] -= obsidianbot_clay_cost
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


def find_max_geodes(
    blueprint: BluePrint, max_minutes: int, bp_id: int, sample: bool
) -> int:
    ore_costs, obsidianbot_clay_cost, geobot_obsidian_cost = blueprint

    initial_bots = (1, 0, 0, 0)
    initial_state = (1, (0, 0, 0, 0), initial_bots, DO_NOTHING)

    prior_states: dict[State, State] = {}
    g_scores: dict[State, int] = {initial_state: 0}
    best_geode_score = 0
    queue = deque([initial_state])

    while queue:
        state = queue.pop()
        time, resources, bots, bot_to_build = state

        if time == max_minutes:
            best_geode_score = max(best_geode_score, g_scores[state])
            continue

        # Collect resources that existing bots generate
        next_resources = list(resources[e] + bots[e] for e in ELEMENTS)

        # Spend resources to build new bots
        next_bots = list(bots)
        if bot_to_build != DO_NOTHING:
            next_bots[bot_to_build] += 1
            next_resources[ORE] -= ore_costs[bot_to_build]
            if bot_to_build == OBSIDIAN:
                next_resources[CLAY] -= obsidianbot_clay_cost
            if bot_to_build == GEODE:
                next_resources[OBSIDIAN] -= geobot_obsidian_cost

        for bot_to_build in get_bot_options(blueprint, bots, next_resources):
            next_state = (
                time + 1,
                tuple(next_resources),
                tuple(next_bots),
                bot_to_build,
            )

            if next_state in g_scores:
                continue

            time_remaining = max_minutes - time
            potential_geodes = (
                next_resources[GEODE]
                + time_remaining * bots[GEODE]
                + time_remaining * (time_remaining + 1) * 0.5
            )
            if potential_geodes < best_geode_score:
                continue

            g_scores[next_state] = next_resources[GEODE] + next_bots[GEODE]
            queue.append(next_state)  # type: ignore
            prior_states[next_state] = state

    retval = max(g_scores.values())
    if not (max_minutes == 32 and not sample):
        correct_answer = (
            SAMPLE_ANSWERS[max_minutes][bp_id] if sample else ACTUAL_ANSWERS[bp_id]
        )
        d, suffix = ("success", "") if retval == correct_answer else ("fail", "_FAIL")
        s = "example" if sample else "actual"
        p = "part1" if max_minutes == 24 else "part2"
        with open(
            os.path.join(
                os.path.dirname(__file__), f"Day19/{d}/{s}s/{s}{bp_id}_{p}{suffix}.txt"
            ),
            "w",
        ) as f:
            with redirect_stdout(f):
                print_path(blueprint, g_scores, prior_states, max_minutes)
        if retval != correct_answer:
            assert False

    return retval


def get_bot_options(blueprint: BluePrint, bots, next_resources) -> set[int]:
    """Determine what bots we should build next"""
    ore_costs, obsidianbot_clay_cost, geobot_obsidian_cost = blueprint
    orebot_ore_cost, claybot_ore_cost, obsidianbot_ore_cost, geobot_ore_cost = ore_costs
    max_ore = max(claybot_ore_cost, obsidianbot_ore_cost, geobot_ore_cost)

    ore, clay, obsidian, _ = next_resources
    need_ore = bots[ORE] < max_ore
    need_clay = bots[CLAY] < obsidianbot_clay_cost
    need_obsidian = bots[OBSIDIAN] < geobot_obsidian_cost
    can_make_ore = ore >= orebot_ore_cost
    can_make_clay = ore >= claybot_ore_cost
    can_make_obsidian = ore >= obsidianbot_ore_cost and clay >= obsidianbot_clay_cost
    can_make_geode = ore >= geobot_ore_cost and obsidian >= geobot_obsidian_cost

    if can_make_geode:
        return {GEODE}

    if need_obsidian and can_make_obsidian:
        if bots[OBSIDIAN]:
            time_to_geode_if_do_nothing = max(
                ceil((geobot_ore_cost - ore) / bots[ORE]),
                ceil((geobot_obsidian_cost - obsidian) / bots[OBSIDIAN]),
            )
            time_to_geode_if_extra_obsidian = max(
                ceil((geobot_ore_cost - ore + obsidianbot_ore_cost) / bots[ORE]),
                ceil((geobot_obsidian_cost - obsidian) / (bots[OBSIDIAN] + 1)),
            )
            if time_to_geode_if_do_nothing < time_to_geode_if_extra_obsidian:
                return {DO_NOTHING}
        return {OBSIDIAN}

    if need_clay and can_make_clay and bots[CLAY]:
        time_to_obsidian_if_do_nothing = max(
            ceil((obsidianbot_ore_cost - ore) / bots[ORE]),
            ceil((obsidianbot_clay_cost - clay) / bots[CLAY]),
        )
        time_to_obsidian_if_extra_clay = max(
            ceil((obsidianbot_ore_cost - ore + claybot_ore_cost) / bots[ORE]),
            ceil((obsidianbot_clay_cost - clay) / (bots[CLAY] + 1)),
        )
        if time_to_obsidian_if_do_nothing < time_to_obsidian_if_extra_clay:
            return {DO_NOTHING}

    bot_options = set()
    if need_clay and can_make_clay:
        bot_options.add(CLAY)
    if need_ore and can_make_ore:
        bot_options.add(ORE)
    bot_options.add(DO_NOTHING)
    return bot_options


from tqdm import tqdm


@print_time_taken
def solve(inputs: str, sample: bool = False) -> None:
    blueprints: dict[int, BluePrint] = {}
    for bp in inputs.splitlines():
        match = re.match(REGEX, bp)
        assert match is not None
        bp_id, ore1, ore2, ore3, ore4, obsidianbot_clay_cost, geobot_obsidian_cost = (
            int(match.groupdict()[x]) for x in ("i", "o1", "o2", "o3", "o4", "cl", "ob")
        )
        blueprints[bp_id] = (
            (ore1, ore2, ore3, ore4),
            obsidianbot_clay_cost,
            geobot_obsidian_cost,
        )

    quality_levels = []
    for bp_id, blueprint in tqdm(blueprints.items()):
        try:
            max_geode = find_max_geodes(blueprint, 24, bp_id, sample)
            quality_levels.append(bp_id * max_geode)
            # print(f"{bp_id}: {max_geode}")
        except AssertionError:
            print(f"{bp_id}: FAIL")

    print(f"Part 1: {sum(quality_levels)}")

    max_geodes = []
    first_3_blueprints = list(blueprints.values())[:3]
    for bp_id, blueprint in tqdm(enumerate(first_3_blueprints, 1)):
        try:
            max_geode = find_max_geodes(blueprint, 32, bp_id, sample)
            max_geodes.append(max_geode)
            print(f"{bp_id}: {max_geode}")
        except AssertionError:
            print(f"{bp_id}: FAIL")

    print(f"Part 2: {prod(max_geodes)}\n")


solve(sample_input, sample=True)
solve(actual_input)
