from __future__ import annotations
import aoc
from aoc.grid import Point
from aoc.utils import adjacent_points
from dataclasses import dataclass
import heapq


@dataclass
class State:
    position: Point
    steps: int = 0
    estimate: int = 0

    def __hash__(self):
        return hash(self.position)
        
    def __eq__(self, other: State):
        return self.position == other.position

    def __lt__(self, other: State):
        return self.estimate < other.estimate
    

def traverse(length: int, points: list[Point]) -> int:
    start, end = Point(0, 0), Point(length-1, length-1)
    stack = []
    heapq.heappush(stack, State(position=start))
    invalid = set(points)

    while stack:
        state: State = heapq.heappop(stack)
        if state.position == end:
            return state.steps
        if state.position in invalid:
            continue
        invalid.add(state.position)

        for adj in set(adjacent_points(state.position)) - invalid:
            if adj.x < 0 or adj.y < 0 or adj.x >= length or adj.y >= length:
                continue
            heapq.heappush(stack, State(position=adj, steps=state.steps+1, estimate=state.steps+1 + adj.manhattan_distance(end)))


@aoc.register(__file__)
def answers():
    data = 'data'
    points = [Point(*map(int, line.split(','))) for line in aoc.read_lines(data)]
    length = 7 if data == 'small' else 71
    portion = 12 if data == 'small' else 2849
    yield traverse(length, points[:portion])

    window = (portion, len(points)-1)
    while window[0] != window[1]:
        idx = window[0] + (window[1] - window[0]) // 2
        result = traverse(length, points[:idx])
        if result is not None:
            window = (idx+1, window[1])
        else:
            window = (window[0], idx-1)
    yield points[window[0]]

if __name__ == '__main__':
    aoc.run()
