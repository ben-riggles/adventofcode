from __future__ import annotations
import aoc
from aoc.grid import Point
from dataclasses import dataclass
import re


@dataclass
class ClawMachine:
    a_button: Point
    b_button: Point
    prize: Point

    def cost(self) -> int:
        ax, ay = self.a_button.x, self.a_button.y
        bx, by = self.b_button.x, self.b_button.y
        px, py = self.prize.x, self.prize.y
        B = ((ax*py - ay*px) / (ax*by - ay*bx))
        A = (px - bx*B) / ax
        cost = A * 3 + B
        return int(cost) if cost.is_integer() else 0
    
    def shift(self, n: int) -> ClawMachine:
        return ClawMachine(self.a_button, self.b_button, self.prize + (n, n))
        
    @staticmethod
    def parse(chunk: str) -> ClawMachine:
        digits = re.findall(r'(\d+)', chunk)
        a_button = Point(int(digits[0]), int(digits[1]))
        b_button = Point(int(digits[2]), int(digits[3]))
        prize = Point(int(digits[4]), int(digits[5]))
        return ClawMachine(a_button, b_button, prize)

@aoc.register(__file__)
def answers():
    machines = [ClawMachine.parse(x) for x in aoc.read_chunks()]
    yield sum(m.cost() for m in machines)
    yield sum(m.shift(10000000000000).cost() for m in machines)

if __name__ == '__main__':
    aoc.run()
