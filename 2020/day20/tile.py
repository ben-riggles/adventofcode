from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import NDArray
import re
from typing import Dict, Iterable, Set

try:
    from .location import Direction
except ImportError:
    from location import Direction


@dataclass
class Tile:
    id: int
    _content: NDArray = field(repr=False)
    _neighbors: Dict[Direction, bool] = field(init=False, repr=False, default_factory=lambda: {d: False for d in Direction})

    def __str__(self):
        content_str = '\n'.join([''.join([char for char in line]) for line in self._content])
        return f'Tile {self.id}:\n{content_str}'

    @property
    def content(self) -> str:
        return self._content[1:-1, 1:-1]

    def edge(self, d: Direction, flipped: bool = False) -> str:
        match d:
            case Direction.ABOVE: edge = self._ar_to_str(self._content[0])
            case Direction.RIGHT: edge = self._ar_to_str(self._content[:, -1])
            case Direction.BELOW: edge = self._ar_to_str(self._content[-1])[::-1]
            case Direction.LEFT:  edge = self._ar_to_str(self._content[:,0])[::-1]
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
        return Tile(self.id, np.rot90(self._content, k=-1*n if clockwise else 1*n))
        
    def flip(self) -> Tile:
        return Tile(self.id, np.flip(self._content, axis=1))

    @staticmethod
    def _ar_to_str(ar: Iterable) -> str:
        return ''.join(ar)

    @staticmethod
    def from_string(tile_str: str) -> Tile:
        lines = tile_str.splitlines()
        id = int(re.match(r'Tile (.*):', lines[0])[1])
        shape = np.array([list(x) for x in lines[1:]])
        return Tile(id=id, _content=shape)