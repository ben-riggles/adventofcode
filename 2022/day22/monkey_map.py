from __future__ import annotations
import aoc
from aoc.utils import pairwise
from dataclasses import dataclass
from enum import Enum
import numpy as np
from numpy.typing import NDArray
import re
from typing import Generator


Point = tuple[int, int]

def locations(truth: NDArray) -> Generator[Point]:
    yield from ((x[1], x[0]) for x in zip(*np.where(truth)))

class CollisionError(Exception):
    pass

class Facing(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def rotate(self, n: int=1, clockwise=True):
        return Facing((self.value + (n if clockwise else -n)) % 4)

class MonkeyMap:
    def __init__(self, map_data: str):
        grid = self._grid(map_data)
        self.start: Point = 0, np.where(grid[0] != ' ')[0][0]
        self._open_tiles = {(y, x) for x, y in locations(grid == '.')}
        self._walls = {(y, x) for x, y in locations(grid == '#')}
        self._shape = grid.shape

    def _grid(self, map_data: str):
        lines = map_data.splitlines()
        max_len = max(len(line) for line in lines)
        return np.array([list(x + ' ' * (max_len - len(x))) for x in map_data.splitlines()])

    def move(self, p: Point, f: Facing) -> Point:
        match f:
            case Facing.UP: mod = (-1, 0)
            case Facing.RIGHT: mod = (0, 1)
            case Facing.DOWN: mod = (1, 0)
            case Facing.LEFT: mod = (0, -1)

        p = (p[0] + mod[0]) % self._shape[0], (p[1] + mod[1]) % self._shape[1]
        if p in self._open_tiles: return p
        if p in self._walls: raise CollisionError
        return self.move(p, f)
    

class CubeMonkeyMap(MonkeyMap):
    class Face:
        def __init__(self, top_left: Point, edge_size: int):
            self.top_left = top_left
            self.edge_size = edge_size
            self.neighbors = {f: None for f in Facing}

        def __repr__(self):
            return f'Face({self.top_left})'

        def __contains__(self, point: Point) -> bool:
            return self.top_left[0] <= point[0] <= self.top_left[0] + self.edge_size and self.top_left[1] <= point[1] <= self.top_left[1] + self.edge_size

    def __init__(self, map_data: str):
        super().__init__(map_data)

        grid = self._grid(map_data)
        edge_size = min(sum(row != ' ') for row in grid)
        self.faces: list[CubeMonkeyMap.Face] = []
        print(grid)
        for y in range(0, len(grid), edge_size):
            for x in range(0, len(grid[0]), edge_size):
                if grid[y][x] != ' ':
                    self.faces.append(CubeMonkeyMap.Face(top_left=(y,x), edge_size=edge_size))
                    
        for face in self.faces:
            neighbor_faces = {
                (face.top_left[0] - edge_size, face.top_left[1]): Facing.UP,
                (face.top_left[0] + edge_size, face.top_left[1]): Facing.DOWN,
                (face.top_left[0], face.top_left[1] - edge_size): Facing.LEFT,
                (face.top_left[0], face.top_left[1] + edge_size): Facing.RIGHT,
            }
            for f in self.faces:
                try:
                    facing = neighbor_faces[f.top_left]
                except KeyError:
                    continue

                face.neighbors[facing] = (f, facing)
                f.neighbors[facing.rotate(2)] = (face, facing)

        two = 2


        
        


def navigate(monkey_map: MonkeyMap, cmds: list[str], facing: Facing) -> tuple[Point, Facing]:
    point = monkey_map.start
    for movements, turn in pairwise(cmds):
        for _ in range(int(movements)):
            try:
                point = monkey_map.move(point, facing)
            except CollisionError:
                break
        facing = facing.rotate(clockwise = turn == 'R')
    return point, facing

def password(point: Point, facing: Facing) -> int:
    return 1000 * (point[0] + 1) + 4 * (point[1] + 1) + facing.value


@aoc.register(__file__)
def answers():
    map_data, cmds = aoc.read_chunks('small')
    cmds = re.split(r'(R|L)', cmds)
    
    monkey_map = MonkeyMap(map_data)
    point, facing = navigate(monkey_map, cmds, Facing.RIGHT)
    yield password(point, facing)

    monkey_map = CubeMonkeyMap(map_data)
    # point, facing = navigate(monkey_map, cmds, Facing.RIGHT)
    # yield password(point, facing)

if __name__ == '__main__':
    aoc.run()
