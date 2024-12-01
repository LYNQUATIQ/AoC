"""https://adventofcode.com/2022/day/19"""

import os
import re

from collections import deque
from math import prod

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day19_input.txt")) as f:
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

# State is a tuple of time, initial bots, initial resources, and bot to build
State = tuple[int, tuple[int, ...], tuple[int, ...], int]


def find_max_geodes(blueprint: BluePrint, max_minutes: int) -> int:
    ore_costs, obsidianbot_clay_cost, geobot_obsidian_cost = blueprint
    max_ore = max(ore_costs[CLAY], ore_costs[OBSIDIAN], ore_costs[GEODE])

    initial_bots = (1, 0, 0, 0)
    initial_state = (1, (0, 0, 0, 0), initial_bots, DO_NOTHING)

    prior_states: dict[State, State] = {}
    end_states: dict[State, int] = {initial_state: 0}
    best_geodes_so_far = 0
    queue = deque([initial_state])

    while queue:
        state = queue.popleft()
        time, resources_at_start, bots_at_start, bot_to_build = state

        # Update resources with output of existing bots and any spend on a new bot
        updated_resources = list(
            resources_at_start[e] + bots_at_start[e] for e in ELEMENTS
        )
        if bot_to_build != DO_NOTHING:
            updated_resources[ORE] -= ore_costs[bot_to_build]
            if bot_to_build == OBSIDIAN:
                updated_resources[CLAY] -= obsidianbot_clay_cost
            if bot_to_build == GEODE:
                updated_resources[OBSIDIAN] -= geobot_obsidian_cost
        next_bots = tuple(
            n + int(i == bot_to_build) for i, n in enumerate(bots_at_start)
        )

        if time == max_minutes:
            end_states[state] = updated_resources[GEODE]
            best_geodes_so_far = max(best_geodes_so_far, updated_resources[GEODE])
            continue

        # Determine what bots could be built and how many minutes it would take
        time_remaining = max_minutes - time
        ore, clay, obsidian, _ = updated_resources
        ore_bots, clay_bots, obsidian_bots, _ = next_bots
        bots_to_build: list[tuple[int, int]] = []
        if obsidian_bots:
            geodoe_minutes = max(
                0,
                -((obsidian - geobot_obsidian_cost) // obsidian_bots),
                -((ore - ore_costs[GEODE]) // ore_bots),
            )
            if geodoe_minutes < time_remaining:
                bots_to_build.append((geodoe_minutes, GEODE))
        if (obsidian_bots < geobot_obsidian_cost) and clay_bots:
            obsidian_minutes = max(
                0,
                -((clay - obsidianbot_clay_cost) // clay_bots),
                -((ore - ore_costs[OBSIDIAN]) // ore_bots),
            )
            if obsidian_minutes < time_remaining:
                bots_to_build.append((obsidian_minutes, OBSIDIAN))
        if clay_bots < obsidianbot_clay_cost:
            clay_minutes = max(0, -((ore - ore_costs[CLAY]) // ore_bots))
            if clay_minutes < time_remaining:
                bots_to_build.append((clay_minutes, CLAY))
        if ore_bots < max_ore:
            ore_minutes = max(0, -((ore - ore_costs[ORE]) // ore_bots))
            if ore_minutes < time_remaining:
                bots_to_build.append((ore_minutes, ORE))
        if ore >= ore_costs[GEODE] and obsidian >= geobot_obsidian_cost:
            # Always make geode immediately if possible
            bots_to_build = [(0, GEODE)]
        if not bots_to_build:
            bots_to_build.append((0, DO_NOTHING))

        for minutes, next_bot_to_build in bots_to_build:
            next_resources = tuple(
                updated_resources[e] + next_bots[e] * minutes for e in ELEMENTS
            )
            next_state = (
                time + minutes + 1,
                next_resources,
                next_bots,
                next_bot_to_build,
            )

            time_remaining = max_minutes - (time + minutes)
            potential_geodes = (
                next_resources[GEODE]
                + time_remaining * next_bots[GEODE]
                + time_remaining * (time_remaining + 1) * 0.5
            )
            if potential_geodes < best_geodes_so_far:
                continue

            queue.append(next_state)  # type: ignore
            prior_states[next_state] = state

    return best_geodes_so_far


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


solve(sample_input)
solve(actual_input)
