import os
import re

from itertools import permutations

with open(os.path.join(os.path.dirname(__file__), "inputs/day13_input.txt")) as f:
    actual_input = f.read()

sample_input = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""


def total_happiness(first_participant, other_participants, happiness_delta):
    n = len(other_participants)
    arrangements = permutations(other_participants)
    max_happiness = 0
    for seating in arrangements:
        happiness = 0
        for i in range(n - 1):
            happiness += happiness_delta.get((seating[i], seating[i + 1]), 0)
            happiness += happiness_delta.get(
                (seating[n - i - 1], seating[n - i - 2]), 0
            )
        happiness += happiness_delta.get((first_participant, seating[0]), 0)
        happiness += happiness_delta.get((first_participant, seating[-1]), 0)
        happiness += happiness_delta.get((seating[0], first_participant), 0)
        happiness += happiness_delta.get((seating[-1], first_participant), 0)
        max_happiness = max(happiness, max_happiness)
    return max_happiness


regex = re.compile(
    r"^(?P<guest>.+) would (?P<gainloss>(gain|lose)) (?P<delta>\d+) happiness units by sitting next to (?P<other>.+)\.$"
)


def solve(inputs):
    guest_list = (regex.match(line).groupdict() for line in inputs.splitlines())

    participants, deltas = set(), {}
    for data in guest_list:
        participants.add(data["guest"])
        deltas[(data["guest"], data["other"])] = {"gain": +1, "lose": -1}[
            data["gainloss"]
        ] * int(data["delta"])
    participants = list(participants)
    print(f"Part 1: {total_happiness(participants[0], participants[1:], deltas)}")
    print(f"Part 2: {total_happiness('me', participants, deltas)}\n")


solve(sample_input)
solve(actual_input)
