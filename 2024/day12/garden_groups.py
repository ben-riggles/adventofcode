from __future__ import annotations
import aoc
from aoc.grid import Grid, Point, Direction
from collections import deque, defaultdict
from dataclasses import dataclass, field
import itertools
from typing import Iterator


class GardenPlot(Grid[str]):
    @dataclass
    class Region:
        plant: str
        points: set[Point] = field(default_factory=set)
        perimeter: int = 0
        sides: int = 0

        def __repr__(self):
            return f'Region(plant={self.plant}, area={self.area}, perimeter={self.perimeter})'

        @property
        def area(self) -> int:
            return len(self.points)
        
        def fence_price(self, discount: bool = False) -> int:
            return self.area * (self.perimeter if not discount else self.sides)
        
    
    @staticmethod
    def __count_sides(direction: Direction, points: list[Point]) -> int:
        diffs = ((direction.rotate(1).movement, direction.rotate(-1).movement))
        sorter = (lambda p: (p.x, p.y)) if direction in (Direction.LEFT, Direction.RIGHT) else (lambda p: (p.y, p.x))
        borders = sorted(points, key=sorter)
        num_sides = 1
        for p1, p2 in itertools.pairwise(borders):
            if not any((p2 == p1 + diffs[0], p2 == p1 + diffs[1])):
                num_sides += 1
        return num_sides
        
    def __map_region(self, point: Point, value: str) -> tuple[GardenPlot.Region, set[Point]]:
        visited = set()
        queue = deque([point])
        region = GardenPlot.Region(plant=value)
        sides = defaultdict(list)

        while queue:
            p = queue.pop()
            if p in visited:
                continue
            visited.add(p)
            region.points.add(p)

            for d in Direction:
                adj = p + d.movement
                if not self.binds(adj):
                    sides[d].append(p)
                elif self[adj] != value:
                    sides[d].append(p)
                    visited.add(adj)
                elif adj not in visited:
                    queue.append(adj)

        region.perimeter = sum(len(x) for x in sides.values())
        region.sides = sum(self.__count_sides(d, x) for d, x in sides.items())
        return region, visited - region.points
        
    def regions(self) -> Iterator[GardenPlot.Region]:
        point = Point(0, 0)
        visited = set()
        queue = {point}

        while queue:
            p = queue.pop()
            plant = self[p]
            region, neighbors = self.__map_region(p, plant)
            yield region

            visited |= region.points
            queue = (queue | neighbors) - visited

@aoc.register(__file__)
def answers():
    garden = GardenPlot(aoc.read_grid())
    regions = tuple(garden.regions())

    yield sum(r.fence_price() for r in regions)
    yield sum(r.fence_price(discount=True) for r in regions)

if __name__ == '__main__':
    aoc.run()
