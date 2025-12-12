from __future__ import annotations
import aoc
from dataclasses import dataclass, field
from itertools import chain, combinations
from functools import reduce
from operator import xor
import scipy


@dataclass
class Machine:
    target: str
    buttons: tuple[tuple[int]] = field(default_factory=tuple, repr=False)
    joltages: tuple[int] = field(default_factory=tuple)

    def start(self) -> int:
        target = self.target.replace('.', '0').replace('#', '1')
        target_n = int(target[::-1], 2)
        buttons_n = [sum(2**x for x in button) for button in self.buttons]
        for buttons in chain.from_iterable(combinations(buttons_n, r) for r in range(1, len(target))):
            value = reduce(xor, buttons)
            if value == target_n:
                return len(buttons)
        raise

    def set_joltage(self) -> int:
        matrix = [[int(i in button) for button in self.buttons] for i in range(len(self.joltages))]
        c = [1] * len(self.buttons)
        presses = scipy.optimize.linprog(c=c, A_eq=matrix, b_eq=self.joltages, integrality=1).x
        return int(sum(presses))
    
    @classmethod
    def from_string(cls, data: str) -> Machine:
        pieces = data.split(' ')
        target = pieces[0][1:-1]
        buttons = tuple(tuple(map(int, x[1:-1].split(','))) for x in pieces[1:-1])
        joltages = pieces[-1][1:-1]
        joltages = tuple(map(int, joltages.split(',')))
        return Machine(target, buttons, joltages)


@aoc.register(__file__)
def answers():
    machines = [Machine.from_string(x) for x in aoc.read_lines()]
    yield sum(x.start() for x in machines)
    yield sum(x.set_joltage() for x in machines)

if __name__ == '__main__':
    aoc.run()
