from utils import print_time_taken


@print_time_taken
def solve(card_public_key, door_public_key):

    # Determine loop size from public key
    # ------------------------------------
    # Public key is a power of 7 (mod 20201227).
    # To determine loop size we count how many times we need to modulo divide key by 7.
    # Because 20201227 is prime we can use the multiplicative inverse of 7 and
    # repeatedly *multiply* by that until we get to 7.
    # We can calculate the multiplicative inverse from Fermat's Little Theorem:
    #                     Multiplicative Inverse of a:  1/a  =  a^(n-2)  (mod n)
    u = pow(7, 20201225, 20201227)
    x, card_loop_size = card_public_key, 1
    while x != 7:
        x = (x * u) % 20201227
        card_loop_size += 1

    print(f"Part 1: {pow(door_public_key, card_loop_size, 20201227)}")


solve(5764801, 17807724)
solve(9232416, 14144084)
