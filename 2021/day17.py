import os

from packet_decoder import BitStream, Packet

with open(os.path.join(os.path.dirname(__file__), f"inputs/day16_input.txt")) as f:
    actual_input = f.read()


SAMPLES_PART1 = {}
SAMPLES_PART2 = {}

p = Packet(BitStream("38006F45291200"))

for sample, answer in SAMPLES_PART1.items():
    assert Packet(BitStream(sample)).version_sum == answer

for sample, answer in SAMPLES_PART2.items():
    assert Packet(BitStream(sample)).value == answer


def solve(inputs):
    packet = Packet(BitStream(inputs))
    print(f"Part 1: {packet.version_sum}")
    print(f"Part 2: {packet.value}\n")


solve(actual_input)
