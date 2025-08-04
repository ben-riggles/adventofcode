from __future__ import annotations
import aoc
from aoc.grid import Point, KeyGrid
from aoc.utils import adjacent_points
from collections import deque, defaultdict
import sys
from typing import Generator


def points_within_distance(p: Point, distance: int):
	for dist in range(1, distance + 1):
		for d in range(dist):
			dd = dist - d
			yield from (p + (dd, d), p + (-dd, -d), p + (d, -dd), p + (-d, dd))


class Racetrack(KeyGrid):
    fields = {
        'start': 'S',
        'end': 'E',
        'wall': '#',
        'track': '.',
    }

    def __post_init__(self):
        self.__build_times()

    @property
    def start(self) -> Point:
        return next(iter(self.points['start']))
    
    @property
    def end(self) -> Point:
        return next(iter(self.points['end']))
    
    def __build_times(self):
        time_map = defaultdict(lambda: sys.maxsize)
        start, end = self.start, self.end
        walls = self.points['wall']
        queue = deque([(end, 0)])

        while queue:
            position, time = queue.popleft()
            if time > time_map[position]:
                continue
            time_map[position] = time

            if position == start:
                continue

            for adj in set(adjacent_points(position)) - walls:
                queue.append((adj, time+1))
        self.time_map: dict[Point, int] = time_map

    def find_cheats(self, cheat_time: int, threshold: int) -> Generator[int]:
        valid_points = set(self.time_map.keys())
        for point, dist in self.time_map.items():
            for cheat in set(points_within_distance(point, cheat_time)) & valid_points:
                cheat_dist = point.manhattan_distance(cheat)
                if (time_saved := dist - self.time_map[cheat] - cheat_dist) >= threshold:
                    yield time_saved


@aoc.register(__file__)
def answers():
    data = 'data'
    racetrack = Racetrack(aoc.read_data(data))
    threshold = 50 if data == 'small' else 100

    yield len(list(racetrack.find_cheats(cheat_time=2, threshold=threshold)))
    yield len(list(racetrack.find_cheats(cheat_time=20, threshold=threshold)))

if __name__ == '__main__':
    aoc.run()
