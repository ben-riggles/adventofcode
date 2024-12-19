from __future__ import annotations
import aoc
from aoc.grid import Point
from collections import Counter
from dataclasses import dataclass
from math import prod
import re


@dataclass
class RestroomRobot:
    location: Point
    velocity: Point

    def move(self, shape: Point) -> RestroomRobot:
        new_loc = (self.location + self.velocity) % shape
        return RestroomRobot(new_loc, self.velocity)
    
    def quadrant(self, shape: Point) -> int:
        mid_x = shape.x // 2
        mid_y = shape.y // 2
        if self.location.x < mid_x and self.location.y < mid_y: return 1
        if self.location.x > mid_x and self.location.y < mid_y: return 2
        if self.location.x < mid_x and self.location.y > mid_y: return 3
        if self.location.x > mid_x and self.location.y > mid_y: return 4
        return None
    
    @staticmethod
    def parse(data: str) -> RestroomRobot:
        digits = tuple(map(int, re.findall(r'(-?\d+)', data)))
        loc = Point(digits[0], digits[1])
        vel = Point(digits[2], digits[3])
        return RestroomRobot(loc, vel)
    
def safety_factor(robots: list[RestroomRobot], shape: Point) -> int:
    quadrants = (r.quadrant(shape) for r in robots)
    scores = Counter(quadrants)
    return prod(v for k, v in scores.items() if k is not None)

def draw(robots: list[RestroomRobot], shape: Point):
    locs = {r.location for r in robots}
    for y, row in enumerate(range(shape.y)):
        row = ''.join('□' if Point(x, y) in locs else ' ' for x in range(shape.x))
        print(row)

@aoc.register(__file__)
def answers():
    robots = [RestroomRobot.parse(x) for x in aoc.read_lines()]
    shape = Point(101, 103)

    safeties = []
    for i in range(10000):
        robots = [r.move(shape) for r in robots]
        safeties.append(safety_factor(robots, shape))
    yield safeties[99]

    min_index = safeties.index(min(safeties))
    yield min_index + 1

if __name__ == '__main__':
    aoc.run()
