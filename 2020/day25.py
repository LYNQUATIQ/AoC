# import logging
from utils import print_time_taken

actual_input = """9232416
14144084"""

sample_input = """5764801
17807724"""


@print_time_taken
def solve(inputs):
    card_public_key, door_public_key = map(int, inputs.splitlines())

    # Determine loop size from public key
    # ------------------------------------
    # Public key is a power of 7 (mod 20201227).
    # To determine loop size we count how many times we need to modulo divide key by 7.
    # Because 20201227 is prime we can use the multiplicative inverse of 7 and
    # repeatedly *multiply* by that until we get to 7self.
    # We can calculate the multiplicative inverse from Fermat's Little Theorem:
    # The multiplicative inverse of a:  1/a = a^(n-2)  (mod n)
    seed = 7
    u = pow(seed, 20201225, 20201227)
    x, loop_size = card_public_key, 1
    while x != seed:
        x = (x * u) % 20201227
        loop_size += 1

    # Calculate encryption key
    encryption_key = 1
    for _ in range(loop_size):
        encryption_key = (encryption_key * door_public_key) % 20201227

    print(f"Part 1: {encryption_key}")


solve(sample_input)
solve(actual_input)
