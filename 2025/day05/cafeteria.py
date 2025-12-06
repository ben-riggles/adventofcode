import aoc
from aoc.utils import Interval
            

@aoc.register(__file__)
def answers():
    ranges, ingredients = aoc.read_chunks()
    ranges = [Interval.parse(x) for x in ranges.splitlines()]
    ingredients = tuple(map(int, ingredients.splitlines()))

    yield sum(any(x in r for r in ranges) for x in ingredients)
    yield sum(len(x) for x in Interval.reduce(ranges))

if __name__ == '__main__':
    aoc.run()
