import aoc
from aoc.grid import KeyGrid, Point, Direction
import functools


class TachyonManifold(KeyGrid):
    fields = {
        'start': 'S',
        'splitter': '^',
    }

    @property
    def start(self) -> Point:
        return next(iter(self['start']))

    def move(self, point: Point) -> tuple[set[Point], bool]:
        new_point = point.move(Direction.DOWN)
        if new_point not in self['splitter']:
            return {new_point}, False
        return {new_point.move(Direction.LEFT), new_point.move(Direction.RIGHT)}, True

    def splits(self) -> int:
        total = 0
        beams = {self.start}

        for _ in range(self.height):
            moves = [self.move(beam) for beam in beams]
            beams = set.union(*[x[0] for x in moves])
            total += sum(x[1] for x in moves)
        return total
    
    def timelines(self) -> int:
        @functools.cache
        def __timelines(point: Point) -> int:
            if point.y >= self.height:
                return 1
            return sum(__timelines(beam) for beam in self.move(point)[0])
        
        return __timelines(self.start)


@aoc.register(__file__)
def answers():
    grid = TachyonManifold(aoc.read_data())
    yield grid.splits()
    yield grid.timelines()

if __name__ == '__main__':
    aoc.run()
