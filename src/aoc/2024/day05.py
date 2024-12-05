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
    rules_input, updates_inputs = inputs.split("\n\n")

    rules = [tuple(map(int, rule.split("|"))) for rule in rules_input.splitlines()]
    updates = [
        list(map(int, update.split(","))) for update in updates_inputs.splitlines()
    ]

    def incorrect_pages(positions):
        for a, b in rules:
            if a in positions and b in positions:
                if positions[a][0] > positions[b][0]:
                    return (a, b)
        return None

    middle_values = 0
    incorrect_updates = []
    for update in updates:
        positions = {value: [pos] for pos, value in enumerate(update)}
        if incorrect_pages(positions) is None:
            middle_values += update[len(update) // 2]
        else:
            incorrect_updates.append(update)

    print(f"Part 1: {middle_values}")

    middle_values = 0
    for update in incorrect_updates:
        positions = {value: [pos, pos + 1] for pos, value in enumerate(update)}
        while pages_to_swap := incorrect_pages(positions):
            a, b = pages_to_swap
            for a, b in rules:
                if a in positions and b in positions:
                    pos_a, a_next = positions[a]
                    pos_b, _ = positions[b]
                    if pos_a > pos_b:
                        a_gap = a_next - pos_a
                        new_pos_b = pos_a + a_gap / 2
                        positions[a] = [pos_a, new_pos_b]
                        positions[b] = [new_pos_b, a_next]
                        break
        # Sort positions by the first item in the value list
        positions = dict(sorted(positions.items(), key=lambda x: x[1][0]))
        corrected_update = list(positions.keys())
        middle_values += corrected_update[len(corrected_update) // 2]

    print(f"Part 2: {middle_values}\n")


solve(example_input)
solve(actual_input)
