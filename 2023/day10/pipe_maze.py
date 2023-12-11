from __future__ import annotations
import aoc
from dataclasses import dataclass
from enum import Enum
import numpy as np
from numpy.typing import NDArray
from typing import Generator


@dataclass
class Point:
    x: int
    y: int

    def __getitem__(self, idx: int) -> int:
        match idx:
            case 0: return self.x
            case 1: return self.y
            case _: raise IndexError

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other) -> Point:
        return Point(self.x + other[0], self.y + other[1])
    
    def move(self, dir: Direction) -> Point:
        return self + dir.value

class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

def locations(truth: NDArray) -> Generator[Point]:
    yield from (Point(x[1], x[0]) for x in zip(*np.where(truth)))

def connectable(dir: Direction) -> set[str]:
    all_pipes = {'|', '-', 'L', 'J', '7', 'F', 'S'}
    match dir:
        case Direction.UP: return all_pipes - {'-', 'L', 'J'}
        case Direction.RIGHT: return all_pipes - {'|', 'L', 'F'}
        case Direction.DOWN: return all_pipes - {'-', '7', 'F'}
        case Direction.LEFT: return all_pipes - {'|', 'J', '7'}
        case _: return all_pipes

def travel(pipe: str, dir: Direction) -> Direction:
    match pipe:
        case '|'|'-': return dir
        case 'L': return Direction.RIGHT if dir == Direction.DOWN else Direction.UP
        case 'J': return Direction.LEFT if dir == Direction.DOWN else Direction.UP
        case '7': return Direction.LEFT if dir == Direction.UP else Direction.DOWN
        case 'F': return Direction.RIGHT if dir == Direction.UP else Direction.DOWN
        case _: return None

def find_loop(grid: NDArray, start: Point) -> set[Point]:
    for dir in Direction:
        point = start + dir.value
        visited = {start}

        while point != start:
            visited |= {point}
            pipe = grid[point.y][point.x]
            if pipe not in connectable(dir):
                break
            dir = travel(pipe, dir)
            point = point + dir.value

        if point == start:
            return visited
    raise

def replace_start(grid: NDArray) -> NDArray:
    truth = grid == 'S'
    s = next(locations(truth))
    adjs = {dir: s + dir.value for dir in Direction}
    values = {dir: grid[p[1]][p[0]] for dir, p in adjs.items()}
    dirs = {dir for dir, value in values.items() if value != '.'}
    
    if Direction.UP in dirs:
        new_val = '|' if Direction.DOWN in dirs else ('J' if Direction.LEFT in dirs else 'L')
    elif Direction.LEFT in dirs:
        new_val = '-' if Direction.RIGHT in dirs else '7'
    else:
        new_val = 'F'
    return np.where(grid == 'S', new_val, grid)

def enclosed_tiles(grid: NDArray, loop: set[Point]) -> set[Point]:
    pts = tuple(list(x) for x in zip(*loop))[::-1]
    _grid = np.full_like(grid, fill_value='.')
    _grid[pts] = grid[pts]
    _grid = replace_start(_grid)

    _grid[_grid == '-'] = '.'
    rolled = np.roll(_grid, -1, axis=1)
    while not np.isin(_grid, ['.', '|', 'J', '7']).all():
        _grid = np.select(
            [(_grid == 'F') & (rolled == 'J'), (_grid == 'F') & (rolled == '7'), 
             (_grid == 'L') & (rolled == 'J'), (_grid == 'L') & (rolled == '7')],
            ['|', '.', '.', '|'],
            _grid
        )
        rolled = np.roll(rolled, -1, axis=1)
    
    count = np.where(_grid == '|', 1, 0)
    count = np.cumsum(count, axis=1)
    count[pts] = 0
    return set(locations(count % 2 == 1))


@aoc.register(__file__)
def answers():
    grid = np.array(aoc.read_grid())
    start = next(locations(grid == 'S'))

    loop = find_loop(grid, start)
    yield len(loop) // 2
    yield len(enclosed_tiles(grid, loop))

if __name__ == '__main__':
    aoc.run()
