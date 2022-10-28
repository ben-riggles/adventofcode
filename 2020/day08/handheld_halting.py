from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, ClassVar


class InfiniteLoopException(Exception):
    def __init__(self, message, acc):
        super().__init__(message)
        self.accumulator = acc

@dataclass
class Instruction(ABC):
    op_str: ClassVar[str] = ''
    value: int
    _run: bool = field(init=False, default=False)

    def __repr__(self):
        return f'Instruction({self.op_str} {self.value})'

    def reset(self):
        self._run = False

    def execute(self, state: Program):
        if self._run:
            raise InfiniteLoopException(f'Instruction at index {state.idx} already run', state.accumulator)
        self._run = True
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


class Program:
    def __init__(self, insts: List[Instruction]):
        self.instructions: List[Instruction] = insts.copy()
        self.accumulator: int = 0
        self.idx: int = 0

    def execute(self) -> int:
        [x.reset() for x in self.instructions]

        while True:
            try:
                self.instructions[self.idx].execute(self)
            except IndexError:
                return self.accumulator


with open('2020/day08/data.txt') as f:
    instructions = [Instruction.from_string(x) for x in f.read().splitlines()]

try:
    Program(instructions).execute()
except InfiniteLoopException as e:
    print(f'PART ONE: {e.accumulator}')


jump_idxs = [idx for idx, i in enumerate(instructions) if isinstance(i, Jump)]
for idx in jump_idxs:
    instructions[idx] = NoOperation(instructions[idx].value)
    try:
        accumulator = Program(instructions).execute()
        break
    except InfiniteLoopException as e:
        instructions[idx] = Jump(instructions[idx].value)
print(f'PART TWO: {accumulator}')
