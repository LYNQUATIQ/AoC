"""https://adventofcode.com/2022/day/19"""
import math
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
# ELEMENTS = (GEODE, OBSIDIAN, CLAY, ORE)  # ...in this order to improve heuristic
ELEMENTS = (ORE, CLAY, OBSIDIAN, GEODE)


# Blueprint is a tuple of ore costs, and the clay and obsidian requirments
BluePrint = tuple[tuple[int, int, int, int], int, int]

# State is a tuple of time, initial bots, initial resources and which bot to build
State = tuple[int, tuple[int, ...], tuple[int, ...], int]

from collections import deque

SAMPLE_ANSWERS = {
    1: 9,
    2: 12,
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
    for state in sorted(path):  # type: ignore
        time, resources, bots, bot_to_build = state
        print(f"\n== Minute {time} ==", state)
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
def find_max_geodes(
    blueprint: BluePrint, max_minutes: int, bp_id: int, sample: bool
) -> int:
    ore_costs, clay_cost, obsidian_cost = blueprint
    initial_bots = (1, 0, 0, 0)
    initial_state = (1, (0, 0, 0, 0), initial_bots, DO_NOTHING)

    prior_states: dict[State, State] = {}
    g_scores: dict[State, int] = {initial_state: 0}

    queue = deque([initial_state])

    # if bp_id != 3:
    #     return ACTUAL_ANSWERS[bp_id]
    while queue:
        state = queue.popleft()
        time, resources, bots, bot_to_build = state

        if time == max_minutes:
            continue

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

        # if state == ((12, (2, 12, 0, 0), (1, 3, 0, 0), DO_NOTHING)):
        #     breakpoint()
        bot_options = get_bot_options(blueprint, bots, next_resources, next_bots)

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
            queue.append(next_state)  # type: ignore
            prior_states[next_state] = state

    correct_answer = SAMPLE_ANSWERS[bp_id] if sample else ACTUAL_ANSWERS[bp_id]
    if max(g_scores.values()) != correct_answer:
        s = "sample" if sample else "case"
        with open(
            os.path.join(os.path.dirname(__file__), f"fails/{s}_{bp_id}_FAIL.txt"), "w"
        ) as f:
            with redirect_stdout(f):
                print_path(blueprint, g_scores, prior_states)
        assert False

    return max(g_scores.values())


def get_bot_options(blueprint: BluePrint, bots, next_resources, next_bots) -> set[int]:
    ore_costs, clay_cost, obsidian_cost = blueprint

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
        return {GEODE}

    if need_obsidian and can_make_obsidian:
        if (
            (obsidian + next_bots[OBSIDIAN]) >= obsidian_cost
            and (ore + next_bots[ORE]) >= ore_costs[GEODE]
            and not ((ore + next_bots[ORE]) >= (ore_costs[GEODE] + ore_costs[OBSIDIAN]))
        ):
            return {DO_NOTHING}
        return {OBSIDIAN}

    if need_clay and can_make_clay and bots[CLAY]:
        time_to_obsidian_if_do_nothing = max(
            math.ceil((ore_costs[OBSIDIAN] - ore) / bots[ORE]),
            math.ceil((clay_cost - clay) / bots[CLAY]),
        )
        time_to_obsidian_if_extra_clay = max(
            math.ceil((ore_costs[OBSIDIAN] - ore + ore_costs[CLAY]) / bots[ORE]),
            math.ceil((clay_cost - clay) / (bots[CLAY] + 1)),
        )
        if time_to_obsidian_if_do_nothing < time_to_obsidian_if_extra_clay:
            return {DO_NOTHING}

    bot_options = set()
    if need_clay and can_make_clay:
        bot_options.add(CLAY)
    if need_ore and can_make_ore:
        bot_options.add(ORE)
    if not bot_options:
        bot_options.add(DO_NOTHING)
    return bot_options


@print_time_taken
def solve(inputs: str, sample: bool = False) -> None:
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
        try:
            max_geode = find_max_geodes(blueprint, 24, bp_id, sample)
            quality_levels.append(bp_id * max_geode)
            print(f"{bp_id}: {max_geode}")
        except AssertionError:
            pass

    print(f"Part 1: {sum(quality_levels)}")

    # first_3_blueprints = list(blueprints.values())[:3]
    # max_geodes = [find_max_geodes(blueprint, 32) for blueprint in first_3_blueprints]
    # print(f"Part 2: {max_geodes}\n")
    # print(f"Part 2: {math.prod(max_geodes)}\n")


solve(sample_input, sample=True)
solve(actual_input)
