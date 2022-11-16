from __future__ import annotations
import aoc
from collections import Counter


class PathingError(Exception):
    pass

class Path:
    def __init__(self, start: 'Cave', end: 'Cave'):
        self.caves = [start]
        self.small_visits = {start: 1}
        self.end = end

    @property
    def complete(self):
        return self.caves[-1] == self.end

    def visit(self, cave: 'Cave') -> 'Path':
        if self.complete:
            raise PathingError('Path already complete')
        elif cave == self.caves[0]:
            raise PathingError('Cannot re-visit the starting cave')
        elif not cave.big and cave in self and 2 in self.small_visits.values():
            raise PathingError('Can only re-visit one small cave')

        new_path = Path(start=self.caves[0], end=self.end)
        new_path.small_visits = self.small_visits.copy()
        new_path.caves = self.caves.copy()

        if not cave.big:
            try:
                new_path.small_visits[cave] += 1
            except KeyError:
                new_path.small_visits[cave] = 1
        new_path.caves.append(cave)
        return new_path

    def __iter__(self):
        return iter(self.caves)

    def __repr__(self):
        return f'Path({", ".join([x.name for x in self])})'

class Cave:
    def __init__(self, name: str):
        self.name = name
        self.big = True if name.isupper() else False
        self.links = set()

    def __repr__(self):
        return f'Cave({self.name})'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: Cave):
        return self.name == other.name

    def link(self, other: Cave):
        self.links.add(other)
        other.links.add(self)
        return self

def num_paths_v1(start: Cave, end: Cave) -> int:
    visited: Counter[Cave] = Counter()
    def count_paths(cave: Cave) -> int:
        if cave == end:
            return 1
        visited[cave] += 1
        caves_to_visit = {c for c in cave.links if c not in visited}
        return sum(count_paths(c) for c in caves_to_visit)

    return count_paths(start)

class Pather:
    def __init__(self, visited: Counter[Cave] = Counter()):
        self.visited: visited

    def _can_visit(self, cave: Cave) -> bool:
        return cave not in self.visited

    def paths(self, start: Cave, end: Cave) -> int:
        if start == end:
            return 1

        self.visited[start] += 1
        caves_to_visit = {c for c in start.links if self._can_visit(c)}
        return sum(Pather(self.visited).paths(c, end) for c in caves_to_visit)

    # def paths(self, target, current_path: Path = None) -> list[Path]:
    #     if not current_path:
    #         current_path = Path(start=self, end=target)

    #     _paths = []
    #     for cave in self.links:
    #         try:
    #             path = current_path.visit(cave)
    #         except PathingError as e:
    #             continue

    #         if path.complete:
    #             _paths.append(path)
    #         else:
    #             _paths.extend(cave.paths(target, path))
    #     return _paths


@aoc.register(__file__)
def answers():
    cave_links = [tuple(x.split('-')) for x in aoc.read_lines()]
    cave_names = set([name for link in cave_links for name in link])
    caves = {name: Cave(name) for name in cave_names}
    for cave_a, cave_b in cave_links:
        caves[cave_a].link(caves[cave_b])

    paths1 = num_paths_v1(caves['start'], caves['end'])

    raise

if __name__ == '__main__':
    aoc.run()
