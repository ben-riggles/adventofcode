from __future__ import annotations
import aoc
import functools
import itertools

    
RockGrid = tuple[str]

def rotate(grid: RockGrid) -> RockGrid:
    return tuple(''.join(reversed(x)) for x in zip(*grid))

def tilt(grid: RockGrid) -> RockGrid:
    def _tilt(line: str) -> str:
        groups = []
        for group in line.split('#'):
            groups.append(''.join(sorted(group)))
        return '#'.join(groups)
    return tuple(_tilt(x) for x in grid)

def load(grid: RockGrid) -> int:
    def _load(line: str) -> int:
        return sum(i for i, x in enumerate(line, 1) if x == 'O')
    return sum(_load(x) for x in grid)

def cycle(grid: RockGrid) -> RockGrid:
    return functools.reduce(lambda g, _: rotate(tilt(g)), range(4), grid)


@aoc.register(__file__)
def answers():
    grid = rotate(aoc.read_lines())
    yield load(tilt(grid))

    visited = list()
    for i in itertools.count():
        if grid in visited:
            loop_start = visited.index(grid)
            loop_cycles = i - loop_start
            break
        visited.append(grid)
        grid = cycle(grid)

    total_cycles = 1000000000
    loop = visited[loop_start:i]
    loop_x = (total_cycles - loop_start) % loop_cycles
    yield load(loop[loop_x])

if __name__ == '__main__':
    aoc.run()
