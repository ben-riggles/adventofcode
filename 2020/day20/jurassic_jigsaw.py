from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
import re
import numpy as np
from numpy.typing import NDArray
from typing import List, Iterable, Dict


class Direction(Enum):
    ABOVE = 0
    RIGHT = 1
    BELOW = 2
    LEFT = 3


@dataclass
class Tile:
    id: int
    shape: NDArray = field(repr=False)
    neighbors: Dict[Direction, Tile] = field(init=False, repr=False, default_factory= lambda: {d: None for d in Direction})

    def __str__(self):
        shape_str = '\n'.join([''.join([char for char in line]) for line in self.shape])
        return f'Tile {self.id}:\n{shape_str}'

    @property
    def edges(self) -> Dict[Direction, Tile]:
        return {d: self._ar_to_str(self.rotate(d.value, clockwise=False).shape[0]) for d in Direction if self.neighbor(d) is None}

    def neighbor(self, direction: Direction) -> Tile | None:
        return self.neighbors[direction]

    def can_attach(self, other: Tile) -> bool:
        other_edges = set(other.edges.values())
        flipped_edges = {edge[::-1] for edge in other_edges}
        return bool(set(self.edges.values()) & (other_edges | flipped_edges))

    def rotate(self, n: int=1, clockwise=True) -> Tile:
        return Tile(self.id, np.rot90(self.shape, k=-1*n if clockwise else 1*n))
        
    def flip(self) -> Tile:
        return Tile(self.id, np.flip(self.shape, axis=1))

    def attach(self, other: Tile) -> bool:
        if any(self.neighbors.values()): raise
        if self._attach(other):
            return True
        other = other.flip()
        return self._attach(other)

    def _attach(self, other: Tile) -> bool:
        my_edges, other_edges = self.edges, {d: edge[::-1] for d, edge in other.edges.items()}
        common_edge = set(my_edges.values()) & set(other_edges.values())
        try:
            common_edge = list(common_edge)[0]
        except IndexError:
            return False

        my_dir = next((d for d, edge in my_edges.items() if edge == common_edge))
        other_dir = next((d for d, edge in other_edges.items() if edge == common_edge))
        two = 2

    @staticmethod
    def _ar_to_str(ar: Iterable) -> str:
        return ''.join([c for c in ar])

    @staticmethod
    def from_string(tile_str: str) -> Tile:
        lines = tile_str.splitlines()
        id = int(re.match(r'Tile (.*):', lines[0])[1])
        shape = np.array([list(x) for x in lines[1:]])
        return Tile(id=id, shape=shape)


with open('2020/day20/data.txt') as f:
    tiles = [Tile.from_string(block) for block in f.read().split('\n\n')]

tile_dict = {t.id: t for t in tiles}
d = {}
for t in tiles:
    d[t.id] = [other.id for other in tiles if other.id != t.id and t.can_attach(other)]

corners = [t for t, n in d.items() if len(n) == 2]
print(corners)
print(corners[0]*corners[1]*corners[2]*corners[3])
