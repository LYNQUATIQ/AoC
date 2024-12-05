"""https://adventofcode.com/2024/day/5"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 5)
example_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def solve(inputs: str):
    input1, input2 = inputs.split("\n\n")
    rules = [tuple(map(int, rule.split("|"))) for rule in input1.splitlines()]
    updates = [list(map(int, update.split(","))) for update in input2.splitlines()]

    def find_breached_rule(
        page_positions: dict[int, tuple[float, float]]
    ) -> tuple[int, int] | None:
        for rule in rules:
            if rule[0] in page_positions and rule[1] in page_positions:
                if page_positions[rule[0]] > page_positions[rule[1]]:
                    return rule
        return None

    correct_middle_values, corrected_middle_values = 0, 0
    for update in updates:
        # Track each page's position (as well as the position of the page after it)
        page_positions = {value: (pos, pos + 1) for pos, value in enumerate(update)}

        breached_rule = find_breached_rule(page_positions)
        if breached_rule is None:
            correct_middle_values += update[len(update) // 2]
            continue

        while breached_rule is not None:
            # Move second page after first placing it halfway between first and next
            a, b = breached_rule
            a_position, position_after_a = page_positions[a]
            new_b_position = a_position + (position_after_a - a_position) / 2
            page_positions[a] = (a_position, new_b_position)
            page_positions[b] = (new_b_position, position_after_a)
            breached_rule = find_breached_rule(page_positions)

        update = list(dict(sorted(page_positions.items(), key=lambda x: x[1])))
        corrected_middle_values += update[len(update) // 2]

    print(f"Part 1: {correct_middle_values}")
    print(f"Part 2: {corrected_middle_values}\n")


solve(example_input)
solve(actual_input)
