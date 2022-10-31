from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, ClassVar, Set


class InfiniteLoopError(Exception):
    def __init__(self, message, acc):
        super().__init__(message)
        self.accumulator = acc

@dataclass
class Instruction(ABC):
    op_str: ClassVar[str] = ''
    value: int

    def execute(self, state: Program):
        return self._execute(state)

    @abstractmethod
    def _execute(self, state: Program):
        pass

    @staticmethod
    def from_string(inst_str: str) -> Instruction:
        op, val = inst_str.split(' ')
        try:
            inst = [x for x in Instruction.__subclasses__() if x.op_str == op][0]
            return inst(int(val))
        except IndexError:
            raise ValueError(f'Invalid operation given: {op}')
        

class Accumulate(Instruction):
    op_str: str = 'acc'

    def _execute(self, state):
        state.accumulator += self.value
        state.idx += 1

class Jump(Instruction):
    op_str: str = 'jmp'

    def _execute(self, state):
        state.idx += self.value

class NoOperation(Instruction):
    op_str: str = 'nop'

    def _execute(self, state):
        state.idx += 1


@dataclass
class Program:
    instructions: List[Instruction]
    accumulator: int = 0
    idx: int = 0
    _executed: Set[int] = field(init=False, repr=False, default_factory=set)

    def execute(self) -> int:
        while True:
            if self.idx in self._executed:
                raise InfiniteLoopError(f'Instruction at index {self.idx} already run', self.accumulator)
            self._executed.add(self.idx)

            try:
                self.instructions[self.idx].execute(self)
            except IndexError:
                return self.accumulator


with open('2020/day08/data.txt') as f:
    instructions = [Instruction.from_string(x) for x in f.read().splitlines()]

try:
    Program(instructions).execute()
except InfiniteLoopError as e:
    print(f'PART ONE: {e.accumulator}')


for idx, inst in enumerate(instructions):
    og = inst.__class__
    if og == Accumulate: continue
    elif og == Jump: instructions[idx] = NoOperation(inst.value)
    elif og == NoOperation: instructions[idx] = Jump(inst.value)

    try:
        accumulator = Program(instructions).execute()
        print(f'PART TWO: {accumulator}')
        break
    except InfiniteLoopError as e:
        instructions[idx] = og(inst.value)
