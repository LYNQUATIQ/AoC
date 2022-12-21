"""https://adventofcode.com/2022/day/19"""
from math import ceil, prod
import os
import re

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


def find_max_geodes(blueprint: BluePrint, max_minutes: int) -> int:
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

    return max(g_scores.values())


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

    quality_levels = [
        bp_id * find_max_geodes(plan, 24) for bp_id, plan in blueprints.items()
    ]
    print(f"Part 1: {sum(quality_levels)}")

    first_3_blueprints = list(blueprints.values())[:3]
    print(f"Part 2: {prod(find_max_geodes(plan, 32) for plan in first_3_blueprints)}\n")


solve(sample_input)  # N.B. First example still fails part 2 (54... not 56)
solve(actual_input)
