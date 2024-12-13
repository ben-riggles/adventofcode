from __future__ import annotations
import aoc
from aoc.grid import Grid, Point, Direction
from collections import deque
from dataclasses import dataclass, field
from functools import reduce
from typing import Iterator


class GardenPlot(Grid[str]):
    @dataclass
    class Region:
        plant: str
        points: set[Point] = field(default_factory=set)
        perimeter: int = 0

        def __repr__(self):
            return f'Region(plant={self.plant}, area={self.area}, perimeter={self.perimeter})'

        @property
        def area(self) -> int:
            return len(self.points)
        
        @property
        def sides(self) -> int:
            edges = tuple((d.movement * 0.5) for d in Direction)
            borders = [{(p + e) for e in edges} for p in self.points]
            borders: set[tuple[Point, Direction]] = reduce(lambda x, y: x ^ y, borders, set())
            border_count = 0
            while borders:
                b = borders.pop()
                border_count += 1
                travel = ((Direction.UP, Direction.DOWN) if isinstance(b.x, int) else (Direction.LEFT, Direction.RIGHT))
                for t in travel:
                    n = b + t.movement
                    while n in borders:
                        borders.remove(n)
                        n += t.movement
            return border_count
        
        def fence_price(self, discount: bool = False) -> int:
            return self.area * (self.perimeter if not discount else self.sides)

        
    def __map_region(self, point: Point, value: str) -> tuple[GardenPlot.Region, set[Point]]:
        visited = set()
        queue = deque([point])
        region = GardenPlot.Region(plant=value)

        while queue:
            p = queue.pop()
            if p in visited:
                continue
            visited.add(p)
            region.points.add(p)

            for adj in {p + d.movement for d in Direction}:
                if not self.binds(adj):
                    region.perimeter += 1
                elif self[adj] != value:
                    region.perimeter += 1
                    visited.add(adj)
                elif adj not in visited:
                    queue.append(adj)
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
    garden = GardenPlot(aoc.read_grid('e'))
    regions = tuple(garden.regions())

    print(regions)
    print([(r, r.sides) for r in regions])

    yield sum(r.fence_price() for r in regions)
    yield sum(r.fence_price(discount=True) for r in regions)

if __name__ == '__main__':
    aoc.run()
