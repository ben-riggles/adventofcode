with open('day12/cave_system.txt') as f:
    cave_links = f.read().splitlines()
cave_links = [tuple(x.split('-')) for x in cave_links]

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

    def __add__(self, other: 'Cave') -> 'Cave':
        self.links.add(other)
        other.links.add(self)
        return self

    def __repr__(self):
        return f'Cave({self.name})'

    def paths(self, target, current_path: Path = None) -> list[Path]:
        if not current_path:
            current_path = Path(start=self, end=target)

        _paths = []
        for cave in self.links:
            try:
                path = current_path.visit(cave)
            except PathingError as e:
                continue

            if path.complete:
                _paths.append(path)
            else:
                _paths.extend(cave.paths(target, path))
        return _paths


cave_names = set([name for link in cave_links for name in link])
caves = {name: Cave(name) for name in cave_names}

for cave_a, cave_b in cave_links:
    caves[cave_a] += caves[cave_b]

paths = caves['start'].paths(caves['end'])
print(paths)
print(len(paths))
