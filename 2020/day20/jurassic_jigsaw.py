from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
import re
import numpy as np
from numpy.typing import NDArray
from typing import Iterable, Dict, Set, Tuple, List


class Direction(Enum):
    ABOVE = 0
    RIGHT = 1
    BELOW = 2
    LEFT = 3

    def __add__(self, value: int) -> Direction:
        v = value.value if isinstance(value, Direction) else value
        return Direction((self.value + v) % 4)

    def __sub__(self, value: int) -> Direction:
        v = value.value if isinstance(value, Direction) else value
        return Direction((self.value - v) % 4)
        

@dataclass
class Location:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, dir: Direction) -> Location:
        match dir:
            case Direction.ABOVE: return Location(self.x, self.y - 1)
            case Direction.RIGHT: return Location(self.x + 1, self.y)
            case Direction.BELOW: return Location(self.x, self.y + 1)
            case Direction.LEFT:  return Location(self.x - 1, self.y)


@dataclass
class Tile:
    id: int
    content: NDArray = field(repr=False)
    neighbors: Dict[Direction, bool] = field(init=False, repr=False, default_factory=lambda: {d: False for d in Direction})

    def __str__(self):
        content_str = '\n'.join([''.join([char for char in line]) for line in self.content])
        return f'Tile {self.id}:\n{content_str}'

    def edge(self, d: Direction, flipped: bool = False) -> str:
        match d:
            case Direction.ABOVE: edge = self._ar_to_str(self.content[0])
            case Direction.RIGHT: edge = self._ar_to_str(self.content[:, -1])
            case Direction.BELOW: edge = self._ar_to_str(self.content[-1])[::-1]
            case Direction.LEFT:  edge = self._ar_to_str(self.content[:,0])[::-1]
        return edge if not flipped else edge[::-1]

    def edges(self, include_flipped: bool = True) -> Set[str]:
        edges = {self.edge(d, flipped=False) for d in Direction if self._neighbors[d] == False}
        if include_flipped:
            edges |= {self.edge(d, flipped=True) for d in Direction if self._neighbors[d] == False}
        return edges

    def direction_of_edge(self, edge: str) -> Direction | None:
        for dir in Direction:
            if self.edge(dir) == edge:
                return dir
        return None

    def can_attach(self, other: Tile) -> str | None:
        try:
            return list(self.edges(include_flipped=False) & other.edges())[0]
        except IndexError:
            None

    def rotate(self, n: int=1, clockwise=True) -> Tile:
        return Tile(self.id, np.rot90(self.content, k=-1*n if clockwise else 1*n))
        
    def flip(self) -> Tile:
        return Tile(self.id, np.flip(self.content, axis=1))

    @staticmethod
    def _ar_to_str(ar: Iterable) -> str:
        return ''.join([c for c in ar])

    @staticmethod
    def from_string(tile_str: str) -> Tile:
        lines = tile_str.splitlines()
        id = int(re.match(r'Tile (.*):', lines[0])[1])
        shape = np.array([list(x) for x in lines[1:]])
        return Tile(id=id, content=shape)


class Puzzle:
    @dataclass
    class _Match:
        control: Tile
        loc: Location
        edge: str

    def __init__(self):
        self.layout: Dict[Location, Tile] = dict()

    def __getitem__(self, loc: Location) -> Tile | None:
        try:
            return self.layout[loc]
        except KeyError:
            return None

    @property
    def width(self):
        return max([loc.x for loc in self.layout.keys()]) + 1

    @property
    def height(self):
        return max([loc.y for loc in self.layout.keys()]) + 1

    def place(self, tile: Tile) -> bool:
        if not self.layout:
            self.layout[Location(0,0)] = tile
            return True
        try:
            match = self._find_match(tile)
        except ValueError:
            return False

        new_loc, new_tile = self._orient(match, tile)
        self.layout[new_loc] = new_tile

        self._mark_neighbors(new_loc)
        if new_loc.x < 0 or new_loc.y < 0:
            self.layout = self._reshape(new_loc)
        return True

    def corners(self) -> List[Tile]:
        width, height = self.width, self.height
        return [
            self.layout[Location(0, 0)], self.layout[Location(width-1, 0)],
            self.layout[Location(0, height-1)], self.layout[Location(width-1, height-1)]
        ]

    def _find_match(self, tile: Tile) -> Puzzle._Match:
        for loc, t in self.layout.items():
            if (edge := t.can_attach(tile)) is not None:
                return Puzzle._Match(control=t, loc=loc, edge=edge)
        raise ValueError(f'No match found for tile: {tile.id}')

    def _orient(self, match: Puzzle._Match, tile: Tile) -> Tuple[Location, Tile]:
        edge, edge_rev = match.edge, match.edge[::-1]
        if edge_rev not in tile.edges(include_flipped=False):
            tile = tile.flip()

        control_dir = match.control.direction_of_edge(edge)
        tile_dir = tile.direction_of_edge(edge_rev)
        target_dir = control_dir + 2
        tile = tile.rotate((target_dir - tile_dir).value)

        target_loc = match.loc.move(control_dir)
        return target_loc, tile

    def _mark_neighbors(self, new_loc: Location):
        tile = self.layout[new_loc]
        for dir in Direction:
            if (neighbor := self[new_loc.move(dir)]) is not None:
                tile.neighbors[dir] = True
                neighbor.neighbors[dir+2] = True

    def _reshape(self, new_loc: Location) -> Dict[Location, Tile]:
        if new_loc.x < 0:
            self.layout = {loc.move(Direction.RIGHT): tile for loc, tile in self.layout.items()}
        if new_loc.y < 0:
            self.layout = {loc.move(Direction.BELOW): tile for loc, tile in self.layout.items()}
        return self.layout



with open('2020/day20/data.txt') as f:
    tiles = [Tile.from_string(block) for block in f.read().split('\n\n')]

puzzle = Puzzle()
while tiles:
    tile = tiles.pop(0)
    if not puzzle.place(tile):
        tiles.append(tile)
two = 2

print(puzzle.width, puzzle.height)
corner_ids = [t.id for t in puzzle.corners()]
print(f'PART ONE: {reduce(lambda x,y: x*y, corner_ids)}')
