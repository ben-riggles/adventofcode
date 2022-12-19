from __future__ import annotations
from abc import ABC
import aoc
from dataclasses import dataclass, field
from itertools import cycle


class CollisionError(Exception):
    pass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point | tuple[int, int]) -> Point:
        try:
            return Point(self.x + other.x, self.y + other.y)
        except AttributeError:
            return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Point | tuple[int, int]) -> Point:
        try:
            return Point(self.x - other.x, self.y - other.y)
        except AttributeError:
            return Point(self.x - other[0], self.y - other[1])


@dataclass
class Map:
    width: int
    height: int = field(default=0, init=False)
    points: set[Point] = field(default_factory=set, init=False, repr=False)

    def place(self, rock: Rock):
        assert(not self & rock)
        self.points |= rock.points
        self.height = max(self.height, max((p.y for p in rock.points)) + 1)

    def __and__(self, other: Map | Rock | set[Point]):
        try:
            return self.points & other.points
        except AttributeError:
            return self.points & other
    

class Rock(ABC):
    SHAPE = None

    def __init__(self, *, points: set[Point] = None, bottom_left: Point = None):
        assert(self.SHAPE is not None)
        if not ((points is None) ^ (bottom_left is None)):
            raise AttributeError

        try:
            self.points = {bottom_left + x for x in self.SHAPE}
        except TypeError:
            self.points = points
    
    def shift(self, map: Map, dir: str) -> Rock:
        shift_mod = 1 if dir == '>' else -1
        new_points = {p + (shift_mod, 0) for p in self.points}
        if any(p.x < 0 or p.x >= map.width for p in new_points):
            raise CollisionError
        if map & new_points:
            raise CollisionError
        return self.__class__(points=new_points)

    def fall(self, map: Map) -> Rock:
        new_points = {p - (0, 1) for p in self.points}
        if any(p.y < 0 for p in new_points):
            raise CollisionError
        if map & new_points:
            raise CollisionError
        return self.__class__(points=new_points)

class HorizontalRock(Rock):
    SHAPE = ((0, 0), (1, 0), (2, 0), (3, 0))

class PlusRock(Rock):
    SHAPE = ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2))

class LRock(Rock):
    SHAPE = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))

class VerticalRock(Rock):
    SHAPE = ((0, 0), (0, 1), (0, 2), (0, 3))

class SquareRock(Rock):
    SHAPE = ((0, 0), (1, 0), (0, 1), (1, 1))


@aoc.register(__file__)
def answers():
    gas_pattern = list(aoc.read_data())
    gas_cycle = cycle(gas_pattern)
    rock_cycle = cycle([
        HorizontalRock, PlusRock, LRock, VerticalRock, SquareRock
    ])

    rock_map = Map(width=7)
    states = {}
    for _ in range(2022):
        new_rock = next(rock_cycle)(bottom_left=Point(x=2, y=rock_map.height + 3))
        while True:
            try:
                new_rock = new_rock.shift(rock_map, next(gas_cycle))
            except CollisionError:
                pass

            try:
                new_rock = new_rock.fall(rock_map)
            except CollisionError:
                rock_map.place(new_rock)
                break
    yield rock_map.height

        

if __name__ == '__main__':
    aoc.run()
