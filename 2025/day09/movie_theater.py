from __future__ import annotations
import aoc
from aoc.grid import Point, LineSegment
import itertools
from typing import Generator


def area(a: Point, b: Point) -> int:
    return (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)

def perimeter(vertices: list[Point]) -> Generator[LineSegment]:
    prev = vertices[-1]
    for point in vertices:
        yield LineSegment(prev, point)
        prev = point

def is_contained(edges: list[LineSegment], p1: Point, p2: Point) -> bool:
    min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
    min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
    for edge in edges:
        if min_x < edge.max_x and max_x > edge.min_x and min_y < edge.max_y and max_y > edge.min_y:
            return False
    return True


@aoc.register(__file__)
def answers():
    red_tiles = [Point(*map(int, x.split(','))) for x in aoc.read_lines()]
    areas = sorted([(area(*p), p) for p in itertools.combinations(red_tiles, 2)], key=lambda x: x[0], reverse=True)
    yield areas[0][0]

    edges = list(perimeter(red_tiles))
    for _area, points in areas:
        if is_contained(edges, *points):
            yield _area
            break

if __name__ == '__main__':
    aoc.run()
