from __future__ import annotations
from abc import ABC, abstractmethod
import aoc
from enum import Enum


class Operation(Enum):
    NOOP = ''
    ADDITION = '+'
    MULTIPLICATION = '*'


class Equation(ABC):
    def __init__(self, eq_list: list[tuple[Operation, int|Equation]]):
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
    def parse(cls, eq_list: list[str]) -> Equation:
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


def main():
    equation_strs = aoc.read_lines()

    equations1 = [EquationLeftToRight.from_string(s) for s in equation_strs]
    part1 = sum([eq.evaluate() for eq in equations1])

    equations2 = [EquationAddPriority.from_string(s) for s in equation_strs]
    part2 = sum([eq.evaluate() for eq in equations2])

    aoc.print_results(part1, part2)

if __name__ == '__main__':
    main()
