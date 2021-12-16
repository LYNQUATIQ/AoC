import math
from abc import ABC, abstractmethod
from typing import Callable, Sequence


class Packet(ABC):
    def __init__(self, version: int) -> None:
        self.version = version
        self.subpackets: list[Packet] = []

    @abstractmethod
    def value(self) -> int:
        """Returns packet value"""

    def version_total(self) -> int:
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
        self.operation: Callable[[Sequence[int]], int] = self.OPERATIONS[operation]

    def add_subpacket(self, packet: Packet):
        self.subpackets.append(packet)

    def value(self) -> int:
        values = [subpacket.value() for subpacket in self.subpackets]
        return self.operation(values)


class PacketReader:
    def __init__(self, input_hex) -> None:
        self.bit_stream: str = "".join("{:04b}".format(int(c, 16)) for c in input_hex)
        self.pointer: int = 0
        self.outer_packet: Packet = self.read_packet()

    def packet_value(self) -> int:
        return self.outer_packet.value()

    def version_sum(self) -> int:
        return self.outer_packet.version_total()

    def read_packet(self) -> Packet:
        version, type_id = self.read_value(3), self.read_value(3)

        if type_id == LiteralPacket.LITERAL_TYPE:
            return LiteralPacket(self.read_literal(), version)

        operator_packet = OperatorPacket(type_id, version)
        length_type = self.read_flag()
        if length_type:
            for _ in range(self.read_value(11)):
                operator_packet.add_subpacket(self.read_packet())
        else:
            length = self.read_value(15)
            packet_end = self.pointer + length
            while self.pointer != packet_end:
                operator_packet.add_subpacket(self.read_packet())
        return operator_packet

    def read_literal(self) -> int:
        bits = ""
        while True:
            leading_bit = self.read_flag()
            bits += self.consume_bits(4)
            if not leading_bit:
                return int(bits, 2)

    def read_value(self, number_of_bits: int) -> int:
        return int(self.consume_bits(number_of_bits), 2)

    def read_flag(self) -> bool:
        return self.consume_bits(1) == "1"

    def consume_bits(self, number_of_bits: int) -> str:
        self.pointer += number_of_bits
        return self.bit_stream[self.pointer - number_of_bits : self.pointer]
