import math
from typing import cast


class BitStream:
    def __init__(self, input_hex) -> None:
        self.bitstream: str = bin(int(input_hex, 16))[2:].zfill(len(input_hex) * 4)
        self.pointer: int = 0

    def read_literal(self) -> int:
        bits = ""
        while True:
            leading_bit = self.read_flag()
            bits += self._consume_bits(4)
            if not leading_bit:
                return int(bits, 2)

    def read_value(self, number_of_bits: int) -> int:
        return int(self._consume_bits(number_of_bits), 2)

    def read_flag(self) -> bool:
        return self._consume_bits(1) == "1"

    def _consume_bits(self, number_of_bits: int) -> str:
        self.pointer += number_of_bits
        return self.bitstream[self.pointer - number_of_bits : self.pointer]


class Packet:
    SUM_TYPE = 0
    PRODUCT_TYPE = 1
    MIN_TYPE = 2
    MAX_TYPE = 3
    LITERAL_TYPE = 4
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

    def __init__(self, bitstream: BitStream) -> None:
        self.subpackets = []
        self.cached_value: int | None = None

        self.version = bitstream.read_value(3)
        self.type_id = bitstream.read_value(3)

        if self.type_id == self.LITERAL_TYPE:
            self.cached_value = bitstream.read_literal()
            return

        if bitstream.read_flag():  # Length type == 1
            packet_count = bitstream.read_value(11)
            for _ in range(packet_count):
                self.subpackets.append(Packet(bitstream))
        else:
            bitstream_offset = bitstream.read_value(15)
            bitstream_end = bitstream.pointer + bitstream_offset
            while bitstream.pointer != bitstream_end:
                self.subpackets.append(Packet(bitstream))

    @property
    def value(self) -> int:
        if self.cached_value is None:
            operation = self.OPERATIONS[self.type_id]
            self.cached_value = operation([p.value for p in self.subpackets])
        return self.cached_value

    @property
    def version_sum(self) -> int:
        return self.version + sum(p.version_sum for p in self.subpackets)
