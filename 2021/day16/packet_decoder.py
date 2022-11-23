from __future__ import annotations
from abc import ABC, abstractmethod
import aoc
from dataclasses import dataclass, field
from functools import reduce
from typing import ClassVar


class PacketParseError(Exception):
    pass

@dataclass
class Packet(ABC):
    version: int
    length: int = field(default=0, repr=False)
    type_id: ClassVar[int] = -1
    TYPE_DICT: ClassVar[dict] = {}

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if (type_id := cls.type_id) >= 0:
            Packet.TYPE_DICT[type_id] = cls

    @property
    @abstractmethod
    def value(self):
        pass

    def read(self, bits: str, start: int, end: int) -> str:
        contents = bits[start:end]
        self.length += end - start
        return contents

    def version_total(self) -> int:
        return self.version

    @staticmethod
    def parse(contents) -> Packet:
        version = int(contents[:3], 2)
        packet_type = int(contents[3:6], 2)
        child_cls = Packet.TYPE_DICT[packet_type]
        return child_cls(version=version, length=6)._parse(contents)

    @abstractmethod
    def _parse(self, contents) -> Packet:
        pass

    # @classmethod
    # def parse(cls, contents) -> Packet:
    #     packet = cls()
    #     packet.version = int(packet.read(contents, 0, 3), 2)
    #     packet_type = int(packet.read(contents, 3, 6), 2)
    #     return packet
    #     child = [x for x in Packet.__subclasses__() if x.type_id == packet_type][0]
    #     return child.parse(contents)

@dataclass
class LiteralPacket(Packet):
    type_id = 4
    stored_value: int = field(default=0)

    @property
    def value(self):
        return self.stored_value

    def _parse(self, contents) -> Packet:
        value_strings = []
        idx = 6
        while True:
            try:
                leading_bit = bool(int(self.read(contents, idx, idx+1), 2))
                val_str = self.read(contents, idx+1, idx+5)
                value_strings.append(val_str)
                idx += 5

                if not leading_bit:
                    break
            except (IndexError, ValueError):
                raise PacketParseError()
        self.stored_value = int(''.join(value_strings), 2)
        return self

@dataclass
class OperatorPacket(Packet, ABC):
    packets: list[Packet] = field(default_factory=list)

    def version_total(self):
        return sum([x.version_total() for x in self.packets]) + self.version

    def read_packet(self, contents: str) -> Packet:
        packet = parse_packet(contents, strip=False)
        self.packets.append(packet)
        self.length += packet.length
        return packet.length

    def _parse(self, contents):
        lenTypeID = int(self.read(contents, 6, 7), 2)
        match(lenTypeID):
            case 0:
                subLength = int(self.read(contents, 7, 22), 2)
                idx = 22
                while idx-22 < subLength:
                    idx += self.read_packet(contents[idx:])
            case 1:
                numPackets = int(self.read(contents, 7, 18), 2)
                idx = 18
                for _ in range(0, numPackets):
                    idx += self.read_packet(contents[idx:])
            case _:
                raise PacketParseError()
        return self
adve

class SumPacket(OperatorPacket):
    type_id = 0
    @property
    def value(self):
        return sum([x.value for x in self.packets])

class ProductPacket(OperatorPacket):
    type_id = 1
    @property
    def value(self):
        return reduce(lambda x, y: x*y, [x.value for x in self.packets])

class MinimumPacket(OperatorPacket):
    type_id = 2
    @property
    def value(self):
        return min([x.value for x in self.packets])

class MaximumPacket(OperatorPacket):
    type_id = 3
    @property
    def value(self):
        return max([x.value for x in self.packets])

class GreaterThanPacket(OperatorPacket):
    type_id = 5
    @property
    def value(self):
        return self.packets[0].value > self.packets[1].value

class LessThanPacket(OperatorPacket):
    type_id = 6
    @property
    def value(self):
        return self.packets[0].value < self.packets[1].value

class EqualToPacket(OperatorPacket):
    type_id = 7
    @property
    def value(self):
        return self.packets[0].value == self.packets[1].value


def parse_packet(ts: str, strip: bool=True) -> Packet:
    if len(ts) < 6:
        raise PacketParseError()

    packet = Packet.parse(ts)
    if strip:
        remainder = packet.length % 4
        remainder = 4 - remainder if remainder else 0
        _ = packet.read(ts, packet.length, packet.length+remainder)
    return packet




@aoc.register(__file__)
def answers():
    transmission = bin(int('F' + aoc.read_data(), 16))[2:]
    transmission = transmission[4:]

    packets = []
    while transmission:
        try:
            packet = parse_packet(transmission)
        except PacketParseError:
            'We had to kill it'
            break
        transmission = transmission[packet.length:]
        packets.append(packet)

    yield sum([x.version_total() for x in packets])
    yield sum([x.value for x in packets])

if __name__ == '__main__':
    aoc.run()
