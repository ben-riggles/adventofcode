import aoc
from math import prod

from tile import Tile
from puzzle import Puzzle


def main():
    aoc.setup(__file__)
    tiles = [Tile.from_string(chunk) for chunk in aoc.read_chunks()]

    puzzle = Puzzle(tiles)
    corner_ids = [t.id for t in puzzle.corners()]
    aoc.answer(1, prod(corner_ids))

    image = puzzle.image
    points = set.union(*[x.points for x in image.sea_monsters()])
    aoc.answer(2, image.count_hash() - len(points))

if __name__ == '__main__':
    main()
