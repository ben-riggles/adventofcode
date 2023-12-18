from __future__ import annotations
import aoc
from dataclasses import dataclass
import heapq
from typing import Generator


@dataclass(frozen=True)
class Crucible:
    min_straights: int
    max_straights: int
    
    @dataclass(frozen=True)
    class State:
        position: aoc.Point
        direction: aoc.Direction = aoc.Direction.RIGHT
        heat_loss: int = 0
        estimate: int = 0

        def __hash__(self):
            return hash((self.position, self.direction))
        
        def __eq__(self, other: Crucible.State):
            return self.position == other.position and self.direction == other.direction

        def __lt__(self, other: Crucible.State):
            return self.estimate < other.estimate

class CityBlockMap(aoc.Grid[int]):
    def _heat_loss(self, p1: aoc.Point, p2: aoc.Point) -> int:
        if p1 == p2: return 0
        if p1[0] == p2[0]:
            step = 1 if p2[1] > p1[1] else -1
            return sum(self[(p1[0], i)] for i in range(p1[1]+step, p2[1]+step, step))
        if p1[1] == p2[1]:
            step = 1 if p2[0] > p1[0] else -1
            return sum(self[(i, p1[1])] for i in range(p1[0]+step, p2[0]+step, step))
        raise ValueError
    
    def _possibilities(self, crucible: Crucible, state: Crucible.State) -> Generator[Crucible.State]:
        dirs = [state.direction.rotate(1), state.direction.rotate(-1)]
        if state.heat_loss == 0:
            dirs = [state.direction] + dirs

        for d in dirs:
            for i in range(crucible.min_straights, crucible.max_straights+1):
                if not self.binds(new_pos := state.position.move(d, n=i)):
                    break
                heat_loss = state.heat_loss + self._heat_loss(state.position, new_pos)
                yield Crucible.State(
                    position = new_pos,
                    direction = d,
                    heat_loss = heat_loss,
                    estimate = heat_loss + new_pos.manhattan_distance(self.bottom_right())
                )

    def travel(self, crucible: Crucible) -> int:
        stack = []
        start, end = aoc.Point(*self.top_left()), aoc.Point(*self.bottom_right())
        visited = set()
        heapq.heappush(stack, Crucible.State(start))

        while stack:
            state: Crucible.State = heapq.heappop(stack)
            if state.position == end:
                return state.heat_loss
            if state in visited:
                continue
            visited.add(state)
            
            for new_state in set(self._possibilities(crucible, state)) - visited:
                heapq.heappush(stack, new_state)


@aoc.register(__file__)
def answers():
    city_map = CityBlockMap(aoc.read_grid(), dtype=int)

    crucible1 = Crucible(1, 3)
    yield city_map.travel(crucible1)

    crucible2 = Crucible(4, 10)
    yield city_map.travel(crucible2)

if __name__ == '__main__':
    aoc.run()
