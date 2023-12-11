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

def closed_loop(grid: NDArray, loop: set[Point], point: Point) -> set[Point]:
    pipe = grid[point.y][point.x]
    bad_dirs = {
        '-': {Direction.UP, Direction.DOWN}, '|': {Direction.LEFT, Direction.RIGHT}, 'L': {Direction.LEFT, Direction.DOWN},
        'J': {Direction.RIGHT, Direction.DOWN}, '7': {Direction.UP, Direction.RIGHT}, 'F': {Direction.LEFT, Direction.UP}
    }
    for d in bad_dirs.get(pipe, set()):
        p = point + d.value
        if p in loop:
            return False
    return True

def enclosed_tiles(grid: NDArray) -> set[Point]:
    _grid = np.full((grid.shape[0]*2 - 1, grid.shape[1]*2 - 1), fill_value='.')
    _grid[::2, ::2] = grid
    _grid = np.pad(_grid, 1, mode='constant', constant_values='.')
    right, left = np.roll(_grid, -1, axis=1), np.roll(_grid, 1, axis=1)
    below, above = np.roll(_grid, -1, axis=0), np.roll(_grid, 1, axis=0)
    
    horiz_pipe = np.logical_and(
        np.isin(left, ['-', 'L', 'F', 'S']),
        np.isin(right, ['-', 'J', '7', 'S'])
    )
    vert_pipe = np.logical_and(
        np.isin(above, ['|', '7', 'F', 'S']),
        np.isin(below, ['|', 'J', 'L', 'S'])
    )
    _grid[horiz_pipe] = '-'
    _grid[vert_pipe] = '|'
    _loop = set(locations(_grid != '.'))
    
    enclosed = set()
    not_enclosed = set()
    to_check = set(locations(_grid)) - _loop

    while to_check:
        point = to_check.pop()
        visited = set()
        queue = {point}
        
        while queue:
            p = queue.pop()
            if p in _loop and closed_loop(_grid, _loop, p):
                continue
            elif p.x < 0 or p.x >= _grid.shape[1] or p.y < 0 or p.y >= _grid.shape[0]:
                not_enclosed |= visited
                break

            visited |= {p}
            if p in enclosed:
                enclosed |= visited
                break
            elif p in not_enclosed:
                not_enclosed |= visited
                break
            queue = queue | ({p + d.value for d in Direction} - visited)
        else:
            enclosed |= visited
        to_check -= visited

    return {p for p in enclosed if p[0] % 2 == 1 and p[1] % 2 == 1}


@aoc.register(__file__)
def answers():
    grid = np.array(aoc.read_grid())
    start = next(locations(grid == 'S'))

    loop = find_loop(grid, start)
    yield len(loop) // 2

    mask = np.zeros_like(grid, dtype=bool)
    pts = tuple(list(x) for x in zip(*loop))[::-1]
    mask[pts] = True
    grid[~mask] = '.'

    min_x, max_x = min(pts[1]), max(pts[1])
    min_y, max_y = min(pts[0]), max(pts[0])
    grid = grid[min_y:max_y+1, min_x:max_x+1]
    yield len(enclosed_tiles(grid))

if __name__ == '__main__':
    aoc.run()
