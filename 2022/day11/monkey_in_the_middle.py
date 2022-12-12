from __future__ import annotations
from typing import Callable, ClassVar
import aoc
from dataclasses import dataclass, field
from functools import lru_cache
import math
import re


def euclidean(a: int, b: int, c: int) -> int:
    gcd = math.gcd(a, b)
    k = int(c/gcd)
    q, r, s, t = [0,0], [a,b], [1,0], [0,1]
    
    while r[-1] != 0:
        quotient = r[-2] / r[-1]
        q.append(math.floor(quotient) if quotient >=0 else math.ceil(quotient))
        r.append(r[-2] - q[-1] * r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])

    s, t = s[-2], t[-2]
    if a*s + b*t == -gcd:
        k = -k
    return s*k


class Item:
    def __init__(self, mod: int, offset: int):
        self.mod = mod
        self.offset = offset % mod

    def __repr__(self):
        return f'Item(mod={self.mod}, offset={self.offset})'

    def __add__(self, val: int) -> Item:
        return Item(mod=self.mod, offset=self.offset + val)

    def __mul__(self, val: int) -> Item:
        return Item(mod=self.mod * val, offset=self.offset * val)

    def __mod__(self, val: int) -> Item:
        x = euclidean(self.mod, -val, -self.offset)
        return Item(mod=math.lcm(self.mod, val), offset=self.mod * x + self.offset)

    @staticmethod
    def create(value: int) -> Item:
        return Item(mod=value, offset=0)

i = Item(63, 6)
print(i % 13)

@dataclass
class Monkey:
    id: int
    test: int = field(repr=False)
    items: list[Item] = field(default_factory=list)
    num_inspects: int = field(init=False, default=0, repr=False)
    _worry: Callable[[int], int] = field(init=False, default_factory=lambda: None, repr=False)
    _throw_target: Callable[[bool], int] = field(init=False, default_factory=lambda: None, repr=False)
    _ALL_MONKEYS: ClassVar[dict[int, Monkey]] = {}

    @classmethod
    def all(cls) -> dict[int, Monkey]:
        return cls._ALL_MONKEYS

    def __post_init__(self):
        Monkey._ALL_MONKEYS[self.id] = self

    def take_turn(self, relief: int):
        self.num_inspects += len(self.items)
        items = [self._worry(x) // relief for x in self.items]
        [self.throw(x) for x in items]
        self.items = []

    def throw(self, item):
        target = self._throw_target(item % self.test == 0)
        Monkey.all()[target].items.append(item)

    @staticmethod
    def parse_op_string(op_str: str) -> Callable[[int], int]:
        m = re.match(r'(.*) (\*|\+) (.*)', op_str).groups()
        op = prod if m[1] == '*' else sum
        return lambda x: op((x if m[0] == 'old' else int(m[0]), x if m[2] == 'old' else int(m[2])))

    @staticmethod
    def from_string(monkey_data: str) -> Monkey:
        regex =  r'Monkey (\d+):\n'
        regex += r'  Starting items: (.*)\n'
        regex += r'  Operation: new = (.*)\n'
        regex += r'  Test: divisible by (\d+)\n'
        regex += r'    If true: throw to monkey (\d+)\n'
        regex += r'    If false: throw to monkey (\d+)'
        m = re.match(regex, monkey_data).groups()
        
        monkey_id, op_str, test_val = int(m[0]), m[2], int(m[3])
        true_throw, false_throw = int(m[4]), int(m[5])
        items = [Item(int(x.strip())) for x in m[1].split(',')]

        retval = Monkey(id=monkey_id, test=test_val, items=items)
        retval._worry = Monkey.parse_op_string(op_str)
        retval._throw_target = lambda x: true_throw if x else false_throw
        return retval

@aoc.register(__file__)
def answers():
    monkeys = [Monkey.from_string(x) for x in aoc.read_chunks('small')]
    print(Monkey.all())

    # for _ in range(2000):
    #     for monkey in monkeys:
    #         monkey.take_turn(relief=1)
    # monkey_business = sorted([x.num_inspects for x in monkeys])[-2:]
    # yield prod(monkey_business)

if __name__ == '__main__':
    #aoc.run()
    pass
