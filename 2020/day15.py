sample_input = [0, 3, 6]
actual_input = [18, 11, 9, 0, 5, 1]


def play_game(seeds, max_rounds):
    prior_turn_spoken = {n: t for t, n in enumerate(seeds, 1)}
    last_number_said = seeds[-1]
    for last_turn in range(len(seeds), max_rounds):
        number = last_turn - prior_turn_spoken.get(last_number_said, last_turn)
        prior_turn_spoken[last_number_said] = last_turn
        last_number_said = number
    return last_number_said


def solve(inputs):
    print(f"Part 1: {play_game(inputs, 2020)}")
    print(f"Part 2: {play_game(inputs, 30000000)}\n")


solve(sample_input)
solve(actual_input)
