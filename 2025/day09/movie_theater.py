import aoc
from aoc.grid import Point
import itertools


def area(a: Point, b: Point) -> int:
    return (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)


@aoc.register(__file__)
def answers():
    points = [Point(*map(int, x.split(','))) for x in aoc.read_lines()]
    areas = sorted(area(*p) for p in itertools.combinations(points, 2))
    yield areas[-1]

if __name__ == '__main__':
    aoc.run()
