sample_input = [0, 3, 6]
actual_input = [18, 11, 9, 0, 5, 1]


def play_game(seeds, max_rounds):
    turn = len(seeds)
    last_spoken = {n: t for t, n in enumerate(seeds, 1)}
    last_number_said = seeds[-1]
    del last_spoken[last_number_said]

    while True:
        try:
            number = turn - last_spoken[last_number_said]
        except KeyError:
            number = 0
        last_spoken[last_number_said] = turn
        turn += 1
        last_number_said = number
        if turn == max_rounds:
            return last_number_said


def solve(inputs):
    print(f"Part 1: {play_game(inputs, 2020)}")
    print(f"Part 2: {play_game(inputs, 30000000)}\n")


solve(sample_input)
solve(actual_input)
