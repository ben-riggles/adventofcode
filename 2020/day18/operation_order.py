from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple


class Operation(Enum):
    NOOP = ''
    ADDITION = '+'
    MULTIPLICATION = '*'

    @classmethod
    def _missing_(cls, _):
        return cls.NOOP


class Equation(ABC):
    def __init__(self, eq_list: List[Tuple[Operation, int|Equation]]):
        self.eq_list = eq_list

    def __add__(self, other: int | Equation) -> int:
        return self.evaluate() + other if isinstance(other, int) else self.evaluate() + other.evaluate()

    def __mul__(self, other: int | Equation) -> int:
        return self.evaluate() * other if isinstance(other, int) else self.evaluate() * other.evaluate()

    def __radd__(self, left: int) -> int:
        return left + self.evaluate()

    def __rmul__(self, left: int) -> int:
        return left * self.evaluate()

    @abstractmethod
    def evaluate(self) -> int:
        pass

    @classmethod
    def parse(cls, eq_list: List[str]) -> Equation:
        op = Operation.NOOP
        retval = []
        while eq_list:
            _next = eq_list.pop(0)

            match _next:
                case '(': retval.append((op, cls.parse(eq_list)))
                case ')': return cls(retval)
                case '+'|'*': op = Operation(_next)
                case _: retval.append((op, int(_next)))
        return cls(retval)

    @classmethod
    def from_string(cls, eq_str: str) -> Equation:
        eq_str = eq_str.replace('(', '( ').replace(')', ' )').split(' ')
        return cls.parse(eq_str)

class EquationLeftToRight(Equation):
    def evaluate(self) -> int:
        retval = 0
        for op, val in self.eq_list:
            match op:
                case Operation.ADDITION: retval += val
                case Operation.MULTIPLICATION: retval *= val
                case _: retval = val
        return retval

class EquationAddPriority(Equation):
    def _next_add_idx(self) -> int | None:
        try:
            return next(idx for idx, x in enumerate(self.eq_list) if x[0] == Operation.ADDITION)
        except StopIteration:
            return None

    def evaluate(self) -> int:
        # Handle addition
        while True:
            if (idx := self._next_add_idx()) is None:
                break
            self.eq_list[idx-1] = (self.eq_list[idx-1][0], self.eq_list[idx-1][1] + self.eq_list[idx][1])
            self.eq_list.pop(idx)

        retval = 0
        for op, val in self.eq_list:
            match op:
                case Operation.ADDITION: raise
                case Operation.MULTIPLICATION: retval *= val
                case _: retval = val
        return retval



with open('2020/day18/data.txt') as f:
    equation_strs = [line for line in f.read().splitlines()]

equations = [EquationLeftToRight.from_string(s) for s in equation_strs]
results = [eq.evaluate() for eq in equations]
print(f'PART ONE: {sum(results)}')

equations = [EquationAddPriority.from_string(s) for s in equation_strs]
results = [eq.evaluate() for eq in equations]
print(f'PART TWO: {sum(results)}')
