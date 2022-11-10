import aoc
from math import prod

try:
    from .location import Direction
    from .image import Image
    from .tile import Tile
    from .puzzle import Puzzle
except ImportError:
    from location import Direction
    from image import Image
    from tile import Tile
    from puzzle import Puzzle


def find_monsters(image: Image):
    for _ in range(2):
        for _ in Direction:
            if monsters := image.sea_monsters():
                return monsters
            image = image.rotate(1)
        image = image.flip()


def main():
    aoc.setup(__file__)
    tiles = [Tile.from_string(chunk) for chunk in aoc.read_chunks()]

    puzzle = Puzzle()
    while tiles:
        tile = tiles.pop(0)
        if not puzzle.place(tile):
            tiles.append(tile)
    corner_ids = [t.id for t in puzzle.corners()]
    aoc.answer(1, prod(corner_ids))

    image = puzzle.image
    sea_monsters = find_monsters(image)
    points = set.union(*[x.points for x in sea_monsters])
    aoc.answer(2, image.count_hash() - len(points))

if __name__ == '__main__':
    main()
