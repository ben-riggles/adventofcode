from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from typing import Tuple, List

from image import Image
from location import Direction, Location
from tile import Tile


class Puzzle:
    @dataclass
    class _Match:
        control: Tile
        loc: Location
        edge: str

    def __init__(self):
        self._layout: NDArray = np.atleast_2d([])

    def __getitem__(self, loc: Location) -> Tile:
        if loc.x < 0 or loc.y < 0:
            raise IndexError('Location must be greater than 0')
        return self._layout[loc.y][loc.x]

    def __setitem__(self, loc: Location, tile: Tile):
        if loc.x < 0:
            self._layout = self._add_blank(Direction.LEFT)
            loc.x = 0
        elif loc.y < 0:
            self._layout = self._add_blank(Direction.ABOVE)
            loc.y = 0
        elif loc.x >= self.width:
            self._layout = self._add_blank(Direction.RIGHT)
        elif loc.y >= self.height:
            self._layout = self._add_blank(Direction.BELOW)
        self._layout[loc.y][loc.x] = tile

    def __str__(self):
        content_str = '\n'.join([' '.join([str(tile.id) for tile in row]) for row in self._layout])
        return content_str

    @property
    def width(self) -> int:
        return self._layout.shape[1]

    @property
    def height(self) -> int:
        return self._layout.shape[0]

    @property
    def image(self) -> Image:
        all_rows = [np.hstack([t.content for t in row]) for row in self._layout]
        content = np.vstack(all_rows)
        return Image(content)

    def place(self, tile: Tile) -> bool:
        if self._layout.size == 0:
            self._layout = np.atleast_2d([tile])
            return True
        try:
            match = self._find_match(tile)
        except ValueError:
            return False

        new_loc, new_tile = self._orient(match, tile)
        self[new_loc] = new_tile
        self._mark_neighbors(new_loc)
        return True

    def corners(self) -> List[Tile]:
        width, height = self.width, self.height
        return [self[Location(0, 0)], self[Location(width-1, 0)], self[Location(0, height-1)], self[Location(width-1, height-1)]]

    def rotate(self, n: int=1, clockwise=True) -> Puzzle:
        retval = Puzzle()
        retval._layout = np.rot90(self._layout, k=-1*n if clockwise else 1*n)
        retval._layout = np.vectorize(lambda t: t.rotate(n, clockwise))(retval._layout)
        return retval
        
    def flip(self) -> Puzzle:
        retval = Puzzle()
        retval._layout = np.flip(self._layout, axis=1)
        retval._layout = np.vectorize(lambda t: t.flip())(retval._layout)
        return retval

    def _add_blank(self, dir: Direction) -> NDArray:
        match dir:
            case Direction.ABOVE: return np.pad(self._layout, ((1,0),(0,0)), mode='constant', constant_values=(None,))
            case Direction.RIGHT: return np.pad(self._layout, ((0,0),(0,1)), mode='constant', constant_values=(None,))
            case Direction.BELOW: return np.pad(self._layout, ((0,1),(0,0)), mode='constant', constant_values=(None,))
            case Direction.LEFT:  return np.pad(self._layout, ((0,0),(1,0)), mode='constant', constant_values=(None,))

    def _find_match(self, tile: Tile) -> Puzzle._Match:
        for y, row in enumerate(self._layout):
            for x, t in enumerate(row):
                if t is None: continue
                if (edge := t.can_attach(tile)) is not None:
                    return Puzzle._Match(control=t, loc=Location(x,y), edge=edge)
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
        tile: Tile = self[new_loc]
        for dir in Direction:
            try:
                if (neighbor := self[new_loc.move(dir)]) is not None:
                    tile._neighbors[dir] = True
                    neighbor._neighbors[dir+2] = True
            except IndexError:
                continue