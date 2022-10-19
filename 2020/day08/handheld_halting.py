from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, List


class InfiniteLoopException(Exception):
    def __init__(self, message, acc):
        super().__init__(message)
        self.accumulator = acc


class Instruction(ABC):
    op_str: str = ''

    def __init__(self, val: int):
        self.value: int = val
        self._run: bool = False

    def __str__(self):
        return f'{self.op_str}({self.value})'

    def __repr__(self):
        return str(self)

    def reset(self):
        self._run = False

    def execute(self, accumulator, idx) -> Tuple[int, int]:
        if self._run:
            raise InfiniteLoopException(f'Instruction at index {idx} already run', accumulator)
        self._run = True
        return self._execute(accumulator, idx)

    @abstractmethod
    def _execute(self, accumulator, idx) -> Tuple[int, int]:
        pass

    @staticmethod
    def create(inst_str: str) -> Instruction:
        op, val = inst_str.split(' ')
        val = int(val)

        if op == Accumulate.op_str: return Accumulate(val)
        if op == Jump.op_str: return Jump(val)
        if op == NoOperation.op_str: return NoOperation(val)
        raise Exception(f'Invalid operation given: {op}')


class Accumulate(Instruction):
    op_str: str = 'acc'

    def _execute(self, accumulator, idx) -> Tuple[int, int]:
        return accumulator + self.value, idx + 1


class Jump(Instruction):
    op_str: str = 'jmp'

    def _execute(self, accumulator, idx) -> Tuple[int, int]:
        return accumulator, idx + self.value


class NoOperation(Instruction):
    op_str: str = 'nop'

    def _execute(self, accumulator, idx) -> Tuple[int, int]:
        return accumulator, idx + 1


def run_program(inst: List[Instruction]) -> int:
    [x.reset() for x in inst]

    accumulator, idx = 0, 0
    while True:
        try:
            accumulator, idx = inst[idx].execute(accumulator, idx)
        except IndexError:
            print(f'Program exited successfully: {accumulator}')
            return accumulator



with open('2020/day08/data.txt') as f:
    instructions = [Instruction.create(x) for x in f.read().splitlines()]

try:
    run_program(instructions)
except InfiniteLoopException as e:
    print(f'PART ONE: {e.accumulator}')


accumulator = None
jump_idxs = [idx for idx, i in enumerate(instructions) if isinstance(i, Jump)]
for idx in jump_idxs:
    instructions[idx] = NoOperation(instructions[idx].value)
    try:
        accumulator = run_program(instructions)
        break
    except InfiniteLoopException as e:
        instructions[idx] = Jump(instructions[idx].value)
print(f'PART TWO: {accumulator}')
