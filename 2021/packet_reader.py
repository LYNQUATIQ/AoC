# import logging
from abc import ABC, abstractmethod
import math
import os


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
    def __init__(self, input_hex) -> None:
        self.bit_stream = "".join("{:04b}".format(int(c, 16)) for c in input_hex)
        self.pointer = 0
        self.outer_packet = self.read_packet()

    def consume_bits(self, n) -> int:
        self.pointer += n
        return self.bit_stream[self.pointer - n : self.pointer]

    def read_bit_value(self, n) -> int:
        return int(self.consume_bits(n), 2)

    def read_bit(self) -> int:
        return self.consume_bits(1) == "1"

    def read_literal(self) -> bool:
        bits = ""
        while True:
            leading_bit = self.read_bit()
            bits += self.consume_bits(4)
            if not leading_bit:
                break
        return int(bits, 2)

    def read_packet(self) -> Packet:
        version, type_id = self.read_bit_value(3), self.read_bit_value(3)

        if type_id == LiteralPacket.LITERAL_TYPE:
            return LiteralPacket(self.read_literal(), version)

        operator_packet = OperatorPacket(type_id, version)
        length_type = self.read_bit()
        if length_type:
            for _ in range(self.read_bit_value(11)):
                operator_packet.add_subpacket(self.read_packet())
        else:
            length = self.read_bit_value(15)
            packet_limit = self.pointer + length
            while self.pointer != packet_limit:
                operator_packet.add_subpacket(self.read_packet())
        return operator_packet

    def version_sum(self):
        return self.outer_packet.version_total()

    def packet_value(self):
        return self.outer_packet.value()
