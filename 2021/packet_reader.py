import math
from abc import ABC, abstractmethod
from typing import Callable, Sequence


class Packet(ABC):
    def __init__(self, version: int, type_id: int) -> None:
        self.version = version
        self.type_id = type_id
        self.subpackets: list[Packet] = []

    @abstractmethod
    def value(self) -> int:
        """Returns packet value"""

    def version_sum(self) -> int:
        return self.version + sum(p.version_sum() for p in self.subpackets)


class LiteralPacket(Packet):
    LITERAL_TYPE = 4

    def __init__(self, literal_value: int, version: int, type_id: int) -> None:
        super().__init__(version, type_id)
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
        SUM_TYPE: lambda x: sum(x),
        PRODUCT_TYPE: lambda x: math.prod(x),
        MIN_TYPE: lambda x: min(x),
        MAX_TYPE: lambda x: max(x),
        GREATER_THAN_TYPE: lambda x: x[0] > x[1],
        LESS_THAN_TYPE: lambda x: x[0] < x[1],
        EQUAL_TO_TYPE: lambda x: x[0] == x[1],
    }

    def __init__(self, operation: int, version: int, type_id: int) -> None:
        super().__init__(version, type_id)
        self.operation: Callable[[Sequence[int]], int] = self.OPERATIONS[operation]

    def add_subpacket(self, packet: Packet):
        self.subpackets.append(packet)

    def value(self) -> int:
        return self.operation([p.value() for p in self.subpackets])


class PacketReader:
    def __init__(self, input_hex) -> None:
        self.bitstream: str = bin(int(input_hex, 16))[2:].zfill(len(input_hex) * 4)
        self.pointer: int = 0
        self.packet: Packet = self._read_packet()

    @property
    def packet_value(self) -> int:
        return self.packet.value()

    @property
    def version_sum(self) -> int:
        return self.packet.version_sum()

    def _read_packet(self) -> Packet:
        version, type_id = self._read_value(3), self._read_value(3)

        if type_id == LiteralPacket.LITERAL_TYPE:
            return LiteralPacket(self._read_literal(), version, type_id)

        operator_packet = OperatorPacket(type_id, version, type_id)
        length_type = self._read_flag()
        if length_type:
            for _ in range(self._read_value(11)):
                operator_packet.add_subpacket(self._read_packet())
        else:
            length = self._read_value(15)
            packet_end = self.pointer + length
            while self.pointer != packet_end:
                operator_packet.add_subpacket(self._read_packet())
        return operator_packet

    def _read_literal(self) -> int:
        bits = ""
        while True:
            leading_bit = self._read_flag()
            bits += self._consume_bits(4)
            if not leading_bit:
                return int(bits, 2)

    def _read_value(self, number_of_bits: int) -> int:
        return int(self._consume_bits(number_of_bits), 2)

    def _read_flag(self) -> bool:
        return self._consume_bits(1) == "1"

    def _consume_bits(self, number_of_bits: int) -> str:
        self.pointer += number_of_bits
        return self.bitstream[self.pointer - number_of_bits : self.pointer]
