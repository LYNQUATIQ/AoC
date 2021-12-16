# import logging
from abc import ABC, abstractmethod
import math
import os


with open(os.path.join(os.path.dirname(__file__), f"inputs/day16_input.txt")) as f:
    actual_input = f.read()


class Packet(ABC):
    def __init__(self, version: int) -> None:
        self.version = version
        self.subpackets = []

    @abstractmethod
    def value(self) -> int:
        """Returns packet value"""

    def version_total(self):
        return self.version + sum(p.version_total() for p in self.subpackets)


class LiteralPacket(Packet):
    LITERAL_TYPE = 4

    def __init__(self, literal_value: int, version: int) -> None:
        super().__init__(version)
        self.literal_value = literal_value

    def value(self) -> int:
        return self.literal_value


class OperatorPacket(Packet):
    SUM_TYPE = 0
    PRODUCT_TYPE = 1
    MIN_TYPE = 2
    MAX_TYPE = 3
    GREATER_THAN_TYPE = 5
    LESS_THAN_TYPE = 6
    EQUAL_TO_TYPE = 7

    OPERATIONS = {
        SUM_TYPE: lambda values: sum(values),
        PRODUCT_TYPE: lambda values: math.prod(values),
        MIN_TYPE: lambda values: min(values),
        MAX_TYPE: lambda values: max(values),
        GREATER_THAN_TYPE: lambda values: values[0] > values[1],
        LESS_THAN_TYPE: lambda values: values[0] < values[1],
        EQUAL_TO_TYPE: lambda values: values[0] == values[1],
    }

    def __init__(self, operation: int, version: int) -> None:
        super().__init__(version)
        self.operation = operation

    def add_subpacket(self, packet):
        self.subpackets.append(packet)

    def value(self) -> int:
        values = [subpacket.value() for subpacket in self.subpackets]
        return self.OPERATIONS[self.operation](values)


class PacketReader:

    HEX_MAP = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    def __init__(self, input_hex) -> None:
        self.bit_stream = ""
        for c in input_hex:
            self.bit_stream += self.HEX_MAP[c]

        self.pointer = 0
        self.outer_packet = self.read_packet()

    def read_bits(self, n) -> int:
        result = 0
        while n:
            n -= 1
            result += self.read_bit() * 2 ** n
        return result

    def read_bit(self) -> int:
        bit = self.bit_stream[self.pointer] == "1"
        self.pointer += 1
        return bit

    def read_literal(self) -> int:
        values = []
        while True:
            leading_bit = self.read_bits(1)
            values.append(self.read_bits(4))
            if not leading_bit:
                break
        return sum(n * 16 ** i for i, n in enumerate(values[::-1]))

    def read_packet(self) -> Packet:
        version, type_id = self.read_bits(3), self.read_bits(3)

        if type_id == LiteralPacket.LITERAL_TYPE:
            return LiteralPacket(self.read_literal(), version)

        operator_packet = OperatorPacket(type_id, version)
        length_type = self.read_bit()
        length = self.read_bits(11 if length_type else 15)
        if length_type:
            for _ in range(length):
                operator_packet.add_subpacket(self.read_packet())
        else:
            packet_limit = self.pointer + length
            while self.pointer != packet_limit:
                operator_packet.add_subpacket(self.read_packet())
        return operator_packet

    def version_sum(self):
        return self.outer_packet.version_total()

    def packet_value(self):
        return self.outer_packet.value()


def solve(inputs):
    pr = PacketReader(inputs)
    print(f"Part 1: {pr.version_sum()}")
    print(f"Part 2: {pr.packet_value()}\n")


SAMPLES = {
    "C200B40A82": 3,  # finds the sum of 1 and 2
    "04005AC33890": 54,  # finds the product of 6 and 9
    "880086C3E88112": 7,  # finds the minimum of 7, 8, and 9
    "CE00C43D881120": 9,  # finds the maximum of 7, 8, and 9
    "D8005AC2A8F0": 1,  # because 5 is less than 15
    "F600BC2D8F": 0,  # because 5 is not greater than 15
    "9C005AC2F8F0": 0,  # because 5 is not equal to 15
    "9C0141080250320F1802104A08": 1,  # because 1 + 3 = 2 * 2
}
for sample, answer in SAMPLES.items():
    assert PacketReader(sample).packet_value() == answer

solve(actual_input)
