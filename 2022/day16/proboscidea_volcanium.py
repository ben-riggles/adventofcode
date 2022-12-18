from __future__ import annotations
from typing import ClassVar
import aoc
from collections import deque
from dataclasses import dataclass, field
import heapq
from functools import lru_cache
import re


@dataclass(eq=True)
class Valve:
    name: str
    flow_rate: int = field(compare=False, repr=False)
    tunnels: set[str] = field(repr=False, default_factory=set, compare=False)
    open: bool = field(default=False, compare=False, repr=False)
    _dists: dict[str, int] = field(default_factory=dict, compare=False, repr=False)
    _ALL: ClassVar[dict[str, Valve]] = {}

    def __hash__(self):
        return hash(self.name)

    def __post_init__(self):
        self.open = True if self.flow_rate == 0 else self.open
        Valve._ALL[self.name] = self

    @lru_cache
    def distance(self, other: Valve) -> int:
        queue = deque([(0, self)])
        visited = set()

        while queue:
            distance, valve = queue.popleft()

            if valve == other:
                return distance
            if valve.name in visited:
                continue
            visited.add(valve.name)

            for adj in valve.tunnels - visited:
                adj_val = Valve._ALL[adj]
                queue.append((distance + 1, adj_val))

    def highest_pressure(self, time: int) -> tuple[Valve, int]:
            base_remaining = {v.name for v in Valve._ALL.values() if not v.open}
            queue = deque([(0, time, self, base_remaining)])
            top_pressure = 0

            while queue:
                pressure, time_left, valve, remaining = queue.popleft()

                if valve.name in remaining:
                    remaining.remove(valve.name)
                    time_left -= 1
                    pressure -= (valve.flow_rate * (time_left))
                if len(remaining) == 0 or time_left <= 0:
                    top_pressure = max(top_pressure, -pressure)
                    continue

                for v in remaining:
                    other = Valve._ALL[v]
                    d = valve.distance(other)
                    queue.append((pressure, time_left-d, other, remaining.copy()))
            return top_pressure

    # def highest_pressure(self, time: int) -> tuple[Valve, int]:
    #         base_remaining = {v.name for v in Valve._ALL.values() if not v.open}
    #         path_stack = []
    #         heapq.heappush(path_stack, (0, 0, self.name, base_remaining, []))
    #        # queue = deque([(0, 0, self, base_remaining)])

    #         while path_stack:
    #             time_spent, neg_pressure, valve, remaining, order = heapq.heappop(path_stack)

    #             valve = Valve._ALL[valve]
    #             if time_spent >= time:
    #                 return -neg_pressure
    #             if valve.name in remaining:
    #                 remaining.remove(valve.name)
    #                 order.append(valve.name)
    #                 time_spent += 1
    #                 neg_pressure -= (valve.flow_rate * (time - time_spent))
    #             if len(remaining) == 0:
    #                 print(order)
    #                 print(time_spent)
    #                 return -neg_pressure

    #             for v in remaining:
    #                 other = Valve._ALL[v]
    #                 d = valve.distance(other)
    #                 heapq.heappush(path_stack, (time_spent + d, neg_pressure, other.name, remaining.copy(), order.copy()))

    @staticmethod
    def from_string(valve_str: str) -> Valve:
        m = re.match(r'Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)', valve_str).groups()
        tunnels = m[2].split(', ')
        return Valve(name=m[0], flow_rate=int(m[1]), tunnels=set(tunnels))


@aoc.register(__file__)
def answers():
    valves = [Valve.from_string(x) for x in aoc.read_lines('small')]
    p = Valve._ALL['AA'].highest_pressure(30)
    print(p)

if __name__ == '__main__':
    aoc.run()
