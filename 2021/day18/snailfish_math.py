import math
from enum import Enum
from abc import ABC, abstractmethod
from itertools import combinations
from copy import deepcopy


class Position(Enum):
    TOP = 0
    FIRST = 1
    SECOND = 2


class SnailfishNumber(ABC):
    def __init__(self, parent:'Pair' = None, position:Position = Position.TOP):
        self.parent:'Pair' = parent
        self.position = position

    def __add__(self, other):
        return Pair(deepcopy(self), deepcopy(other))

    @abstractmethod
    def leftmost(self) -> 'Literal': pass

    @abstractmethod
    def rightmost(self) -> 'Literal': pass
    
    @abstractmethod
    def explode(self) -> 'SnailfishNumber': pass

    @abstractmethod
    def split(self) -> 'SnailfishNumber': pass

    @abstractmethod
    def magnitude(self) -> int: pass

    def reduce(self) -> None:
        while True:
            if self.explode() is not None:
                continue
            if self.split() is not None:
                continue
            break
        return self


class Literal(SnailfishNumber):
    def __init__(self, value, parent:'Pair' = None, position:Position = Position.TOP):
        super().__init__(parent, position)
        self.value:int = int(value)

    def __repr__(self):
        return f'{self.value}'

    def leftmost(self):
        return self

    def rightmost(self):
        return self

    @property
    def left(self) -> 'Literal':
        if self.position == Position.SECOND:
            return self.parent.first.rightmost()
        elif self.position == Position.FIRST:
            ancestor = self.parent
            while (ancestor is not None and ancestor.position == Position.FIRST):
                ancestor = ancestor.parent
            return None if ancestor is None or ancestor.position == Position.TOP else ancestor.parent.first.rightmost()
        return None

    @property
    def right(self) -> 'Literal':
        if self.position == Position.FIRST:
            return self.parent.second.leftmost()
        elif self.position == Position.SECOND:
            ancestor = self.parent
            while (ancestor is not None and ancestor.position == Position.SECOND):
                ancestor = ancestor.parent
            return None if ancestor is None or ancestor.position == Position.TOP else ancestor.parent.second.leftmost()
        return None

    def explode(self) -> 'SnailfishNumber':
        return None

    def split(self) -> 'SnailfishNumber':
        if self.value < 10:
            return None
        half = self.value / 2.0
        first, second = Literal(math.floor(half)), Literal(math.ceil(half))
        return Pair(first, second, parent=self.parent, position=self.position)

    def magnitude(self) -> int:
        return self.value


class Pair(SnailfishNumber):
    def __init__(self, first, second, parent:'Pair' = None, position:Position = Position.TOP):
        super().__init__(parent, position)

        self.first:SnailfishNumber = first
        self.first.position = Position.FIRST
        self.first.parent = self

        self.second:SnailfishNumber = second
        self.second.position = Position.SECOND
        self.second.parent = self

    def __repr__(self):
        return f'[{self.first}, {self.second}]'

    def leftmost(self):
        return self.first.leftmost()

    def rightmost(self):
        return self.second.rightmost()

    def split(self) -> 'SnailfishNumber':
        if (pair := self.first.split()) is None:
            if (pair := self.second.split()) is None:
                return None
        if pair.parent == self:
            if pair.position == Position.FIRST:
                self.first = pair
            else:
                self.second = pair
        return pair

    def explode(self) -> 'SnailfishNumber':
        if (result := self.first.explode()) is None:
            result = self.second.explode()

        if result is not None:
            if result.parent == self:
                if result.position == Position.FIRST:
                    self.first = result
                else:
                    self.second = result
            return result

        try:
            ancestor = self.parent.parent.parent.parent
        except AttributeError:
            return None
        if ancestor is None:
            return None

        if left := self.first.left:
            left.value += self.first.value
        if right := self.second.right:
            right.value += self.second.value
        return Literal(0, parent=self.parent, position=self.position)

    def magnitude(self) -> int:
        return 3 * self.first.magnitude() + 2 * self.second.magnitude()


def parse_number(num_str:str):
    while num_str[0] in [']', ',']:
        num_str = num_str[1:]

    if num_str[0].isdigit():
        val = num_str[0]
        retval = Literal(val)
        num_str = num_str[1:]
        return retval, num_str

    num_str = num_str[1:len(num_str)]
    first, num_str = parse_number(num_str)
    second, num_str = parse_number(num_str)
    return Pair(first, second), num_str


with open('2021/day18/numbers.txt') as f:
    numbers = f.read().splitlines()
numbers = [parse_number(x)[0] for x in numbers]

sum = None
for num in numbers:
    if sum is None:
        sum = num
        continue
    sum = sum + num
    sum.reduce()

print(f'Final sum: {sum}')
print(f'Magnitude: {sum.magnitude()}')


largest_mag = 0
for x, y in combinations(numbers, 2):
    sumA, sumB = x + y, y + x
    mag = max(sumA.reduce().magnitude(), sumB.reduce().magnitude())
    largest_mag = max(mag, largest_mag)
print(f'Largest Magnitude: {largest_mag}')