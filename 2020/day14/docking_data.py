from __future__ import annotations
from abc import ABC, abstractmethod
import aoc
from dataclasses import dataclass
import numpy as np
import re
from typing import Type


class Mask:
    def __init__(self, mask_str: str, masks: dict[int, int] = None):
        self._mask_str = mask_str
        self.bit_masks = masks

    def __str__(self):
        return self._mask_str

    @staticmethod
    def from_string(mask_str: str) -> Mask:
        return Mask(
            mask_str = mask_str,
            masks = {2 ** idx: x for idx, x in enumerate(reversed(mask_str))}
        )


@dataclass
class Memory(ABC):
    address: int
    value: int

    @abstractmethod
    def evaluate(self, mask: Mask) -> dict[int, int]:
        pass

class MemoryV1(Memory):
    def evaluate(self, mask):
        retval = self.value
        for x, bit in mask.bit_masks.items():
            try:
                retval = retval | x if int(bit) else retval & ~x
            except ValueError:
                continue
        return {self.address: retval}

class MemoryV2(Memory):
    def evaluate(self, mask):
        address_str = bin(self.address)[2:].zfill(36)
        mask_bits = np.array(list(str(mask)))
        adr_bits = np.array(list(address_str))

        adr_bits = np.where(np.logical_or(adr_bits == 'X', mask_bits == 'X'), 'X', adr_bits)
        adr_bits = np.where(np.logical_and(adr_bits != 'X', mask_bits == '1'), '1', adr_bits)

        addresses = np.array([0], dtype=np.longlong)
        for idx, val in enumerate(reversed(adr_bits)):
            if val == 'X':
                addresses = np.concatenate((addresses, addresses + 2 ** idx))
            else:
                addresses += (2 ** idx) * int(val)
        return {x: self.value for x in addresses}
        

class Program:
    def __init__(self, mem_type):
        self._memory_type: Type[Memory] = mem_type
        self.mask = None
        self.memory: dict[int, int] = {}

    def execute(self, cmd_list: list[str]) -> int:
        [self._execute(x) for x in cmd_list]
        return sum(self.memory.values())

    def _execute(self, cmd: str):
        try:
            mem_data = re.match(r'mem\[(?P<address>.*)\] = (?P<value>.*)', cmd).groupdict()
            return self.memory.update(
                self._memory_type(address=int(mem_data['address']), value=int(mem_data['value'])).evaluate(self.mask))
        except AttributeError:
            pass

        mask_data = re.match(r'mask = (?P<value>.*)', cmd).group(1)
        self.mask = Mask.from_string(mask_data)


def main():
    commands = aoc.read_lines()
    part1 = Program(mem_type=MemoryV1).execute(commands)
    part2 = Program(mem_type=MemoryV2).execute(commands)
    aoc.print_results(part1, part2)

if __name__ == '__main__':
    main()
