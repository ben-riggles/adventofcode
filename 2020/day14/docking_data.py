from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
import math
import numpy as np
from operator import iand
import re
from typing import Dict, List, Type


class Mask:
    X_MASK = 'X'

    def __init__(self, mask_str: str, masks: Dict[int, int] = None):
        self._mask_str = mask_str
        self.bit_masks = masks

    def __str__(self):
        return self._mask_str

    @staticmethod
    def parse(mask_str: str) -> Mask:
        return Mask(
            mask_str = mask_str,
            masks = {int(math.pow(2, int(idx))): x for idx,x in enumerate(reversed(mask_str))}
        )


@dataclass
class Memory(ABC):
    address: int
    value: int

    @abstractmethod
    def evaluate(self, mask: Mask) -> Dict[int, int]:
        pass

class MemoryV1(Memory):
    def evaluate(self, mask: Mask) -> Dict[int, int]:
        retval = self.value
        for x, bit in mask.bit_masks.items():
            if bit == Mask.X_MASK:
                continue
            retval = retval | x if int(bit) else retval & ~x
        return {self.address: retval}

class MemoryV2(Memory):
    def evaluate(self, mask: Mask) -> Dict[int, int]:
        address_str = bin(self.address)[2:].zfill(36)
        mask_bits = np.array(list(str(mask)))
        adr_bits = np.array(list(address_str))

        adr_bits = np.where(np.logical_or(adr_bits == 'X', mask_bits == 'X'), 'X', adr_bits)
        adr_bits = np.where(np.logical_and(adr_bits != 'X', mask_bits == '1'), '1', adr_bits)

        addresses = np.array([0], dtype=np.longlong)
        for idx, val in enumerate(reversed(adr_bits)):
            power = int(math.pow(2, idx))
            if val == 'X':
                addresses = np.concatenate((addresses, addresses + power))
            else:
                addresses += power*int(val)
        return {x: self.value for x in addresses}
        

class Program:
    def __init__(self, mem_type):
        self._memory_type: Type[Memory] = mem_type
        self.mask = None
        self.memory: Dict[int, int] = {}

    def execute(self, cmd_list: List[str]):
        # [self._execute(x) for x in cmd_list]
        for itr, cmd in enumerate(cmd_list):
            if itr == 66:
                two = 2
            self._execute(cmd)
        return self

    def _execute(self, cmd: str):
        m = re.match(r'mem\[(?P<address>.*)\] = (?P<value>.*)', cmd)
        if m is not None:
            return self._update_memory(int(m.group('address')), int(m.group('value')))

        m = re.match(r'mask = (?P<value>.*)', cmd)
        if m is not None:
            return self._update_mask(m.group('value'))

        raise Exception(f'Invalid command given: {cmd}')
    
    def _update_memory(self, address: int, value: int):
        self.memory.update(self._memory_type(address=address, value=value).evaluate(self.mask))

    def _update_mask(self, value: str):
        self.mask = Mask.parse(value)


with open('2020/day14/data.txt') as f:
    commands = f.read().splitlines()

program1 = Program(mem_type=MemoryV1).execute(commands)
print(f'PART ONE: {sum(program1.memory.values())}')

program2 = Program(mem_type=MemoryV2).execute(commands)
print(f'PART TWO: {sum(program2.memory.values())}')