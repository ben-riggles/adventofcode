from __future__ import annotations
import aoc
from aoc.grid import KeyGrid, Point, Direction
from collections import defaultdict
from dataclasses import dataclass, field
import heapq
import sys
from typing import Generator


class ReindeerMaze(KeyGrid):
    fields = {
        'wall': '#',
        'start': 'S',
        'end': 'E'
    }

    @dataclass(frozen=True)
    class State:
        position: Point
        direction: Direction
        score: int = 0
        path: set[Point] = field(repr=False, default_factory=set)

        def __hash__(self):
            return hash((self.position, self.direction))
        
        def __eq__(self, other: ReindeerMaze.State):
            return self.position == other.position and self.direction == other.direction

        def __lt__(self, other: ReindeerMaze.State):
            return self.score < other.score

    @property
    def start(self) -> Point:
        return next(iter(self.points['start']))
    
    @property
    def end(self) -> Point:
        return next(iter(self.points['end']))
    
    def __possibilities(self, state: ReindeerMaze.State) -> Generator[ReindeerMaze.State]:
        next_pt = state.position.move(state.direction)
        if next_pt not in self['wall'] and next_pt not in state.path:
            yield ReindeerMaze.State(next_pt, state.direction, state.score + 1, path=state.path | {next_pt})

        for d in (state.direction.rotate(clockwise=True), state.direction.rotate(clockwise=False)):
            next_pt = state.position.move(d)
            if next_pt not in self['wall'] and next_pt not in state.path:
                yield ReindeerMaze.State(next_pt, d, state.score + 1001, path=state.path | {next_pt})
    
    def best_paths(self) -> list[ReindeerMaze.State]:
        start, end = self.start, self.end
        stack = []
        distance = defaultdict(lambda: sys.maxsize)
        heapq.heappush(stack, ReindeerMaze.State(position=start, direction=Direction.RIGHT, path={start}))
        lowest_score = 0
        best_paths = list()

        while stack:
            state: ReindeerMaze.State = heapq.heappop(stack)
            if lowest_score and state.score > lowest_score:
                break
            if state.position == end:
                lowest_score = state.score
                best_paths.append(state)
                continue

            if distance[state] < state.score:
                continue
            distance[state] = state.score
            
            for new_state in set(self.__possibilities(state)):
                heapq.heappush(stack, new_state)
        return best_paths


@aoc.register(__file__)
def answers():
    grid = ReindeerMaze(aoc.read_data())
    paths = grid.best_paths()
    yield paths[0].score

    all_points = set.union(*[x.path for x in paths])
    yield(len(all_points))

if __name__ == '__main__':
    aoc.run()
