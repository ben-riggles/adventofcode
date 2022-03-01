from abc import ABC, abstractmethod
import numpy as np
from functools import reduce

with open('day16/transmission.txt') as f:
    transmission = f.read().strip()
print(transmission)
transmission = bin(int('F' + transmission, 16))[2:]
transmission = transmission[4:]


class PacketParseError(Exception):
    pass


class Packet(ABC):
    def __init__(self):
        self.version: int
        self.type: int
        self.length:int = 0

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def read(self, bits, start, end):
        contents = bits[start:end]
        self.length += end - start
        return contents

    def version_total(self):
        return self.version

    @property
    @abstractmethod
    def value(self):
        pass

    @classmethod
    @abstractmethod
    def parse(cls, contents):
        pass


class LiteralPacket(Packet):
    def __init__(self):
        super().__init__()
        self.stored_value: int

    @property
    def value(self):
        return self.stored_value

    @classmethod
    def parse(cls, contents):
        packet = cls()
        packet.version = int(packet.read(contents, 0, 3), 2)
        packet.type = int(packet.read(contents, 3, 6), 2)

        value_strings = []
        parsing = True
        idx = 6
        while parsing:
            try:
                parsing = bool(int(packet.read(contents, idx, idx+1), 2))
                val_str = packet.read(contents, idx+1, idx+5)
                value_strings.append(val_str)
                idx += 5
            except (IndexError, ValueError):
                raise PacketParseError()
        packet.stored_value = int(''.join(value_strings), 2)
        return packet


class OperatorPacket(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.packets = []

    def version_total(self):
        return sum([x.version_total() for x in self.packets]) + self.version

    def read_packet(self, contents):
        packet = parse_packet(contents, strip=False)
        self.packets.append(packet)
        self.length += packet.length
        return packet.length

    @classmethod
    def parse(cls, contents):
        packet = cls()
        packet.version = int(packet.read(contents, 0, 3), 2)
        packet.type = int(packet.read(contents, 3, 6), 2)

        lenTypeID = int(packet.read(contents, 6, 7), 2)
        if lenTypeID == 0:
            subLength = int(packet.read(contents, 7, 22), 2)
            idx = 22
            while idx-22 < subLength:
                idx += packet.read_packet(contents[idx:])
        elif lenTypeID == 1:
            numPackets = int(packet.read(contents, 7, 18), 2)
            idx = 18
            for _ in range(0, numPackets):
                idx += packet.read_packet(contents[idx:])
        else:
            raise PacketParseError()
        return packet


class SumPacket(OperatorPacket):
    @property
    def value(self):
        return sum([x.value for x in self.packets])

class ProductPacket(OperatorPacket):
    @property
    def value(self):
        return reduce(lambda x, y: x*y, [x.value for x in self.packets])

class MinimumPacket(OperatorPacket):
    @property
    def value(self):
        return min([x.value for x in self.packets])

class MaximumPacket(OperatorPacket):
    @property
    def value(self):
        return max([x.value for x in self.packets])

class GreaterThanPacket(OperatorPacket):
    @property
    def value(self):
        return 1 if self.packets[0].value > self.packets[1].value else 0

class LessThanPacket(OperatorPacket):
    @property
    def value(self):
        return 1 if self.packets[0].value < self.packets[1].value else 0

class EqualToPacket(OperatorPacket):
    @property
    def value(self):
        return 1 if self.packets[0].value == self.packets[1].value else 0


type_dict = {
    0: SumPacket,
    1: ProductPacket,
    2: MinimumPacket,
    3: MaximumPacket,
    4: LiteralPacket,
    5: GreaterThanPacket,
    6: LessThanPacket,
    7: EqualToPacket
}


def parse_packet(ts, strip=True):
    if len(ts) < 6:
        raise PacketParseError()
    packet_type = int(ts[3:6], 2)

    packet_type = type_dict[packet_type]
    packet = packet_type.parse(ts)

    if strip:
        remainder = packet.length % 4
        remainder = 4 - remainder if remainder else 0
        _ = packet.read(ts, packet.length, packet.length+remainder)
    return packet



packets = []
while transmission:
    try:
        packet = parse_packet(transmission)
    except PacketParseError:
        'We had to kill it'
        break
    transmission = transmission[packet.length:]
    packets.append(packet)


print(f'Number of packets: {len(packets)}')
version_sum = sum([x.version_total() for x in packets])
print(f'Version sum: {version_sum}')
value_sum = sum([x.value for x in packets])
print(f'Value: {value_sum}')