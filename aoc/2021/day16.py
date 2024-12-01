"""https://adventofcode.com/2021/day/16"""

import os

from packet_decoder import BitStream, Packet

with open(os.path.join(os.path.dirname(__file__), "inputs/day16_input.txt")) as f:
    actual_input = f.read()


SAMPLES_PART1 = {
    "8A004A801A8002F478": 16,
    "620080001611562C8802118E34": 12,
    "C0015000016115A2E0802F182340": 23,
    "A0016C880162017C3686B18A3D4780": 31,
}
SAMPLES_PART2 = {
    "C200B40A82": 3,  # finds the sum of 1 and 2
    "04005AC33890": 54,  # finds the product of 6 and 9
    "880086C3E88112": 7,  # finds the minimum of 7, 8, and 9
    "CE00C43D881120": 9,  # finds the maximum of 7, 8, and 9
    "D8005AC2A8F0": 1,  # because 5 is less than 15
    "F600BC2D8F": 0,  # because 5 is not greater than 15
    "9C005AC2F8F0": 0,  # because 5 is not equal to 15
    "9C0141080250320F1802104A08": 1,  # because 1 + 3 = 2 * 2
}

for sample, answer in SAMPLES_PART1.items():
    assert Packet(BitStream(sample)).version_sum == answer

for sample, answer in SAMPLES_PART2.items():
    assert Packet(BitStream(sample)).value == answer


def solve(inputs):
    packet = Packet(BitStream(inputs))
    print(f"Part 1: {packet.version_sum}")
    print(f"Part 2: {packet.value}\n")


solve(actual_input)
