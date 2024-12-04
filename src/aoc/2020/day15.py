from utils import print_time_taken

example_input = [0, 3, 6]
actual_input = [18, 11, 9, 0, 5, 1]


def play_game(seeds, max_rounds):
    last_seen = {n: t for t, n in enumerate(seeds, 1)}
    last_number = seeds[-1]
    for last_turn in range(len(seeds), max_rounds):
        next_number = last_turn - last_seen.get(last_number, last_turn)
        last_seen[last_number] = last_turn
        last_number = next_number
    return last_number


@print_time_taken
def solve(inputs):
    print(f"Part 1: {play_game(inputs, 2020)}")
    print(f"Part 2: {play_game(inputs, 30_000_000)}\n")


solve(example_input)
solve(actual_input)
