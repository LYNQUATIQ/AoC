from utils import print_time_taken


@print_time_taken
def solve(card_public_key, door_public_key):
    x, card_private_key = 7, 1
    while x != card_public_key:
        x = (x * 7) % 20201227
        card_private_key += 1
    print(f"Part 1: {pow(door_public_key, card_private_key, 20201227)}")


solve(5764801, 17807724)
solve(9232416, 14144084)
