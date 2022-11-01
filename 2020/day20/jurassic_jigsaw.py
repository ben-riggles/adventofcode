from functools import reduce

from location import Direction
from image import Image
from tile import Tile
from puzzle import Puzzle


with open('2020/day20/data.txt') as f:
    tiles = [Tile.from_string(block) for block in f.read().split('\n\n')]

puzzle = Puzzle()
while tiles:
    tile = tiles.pop(0)
    if not puzzle.place(tile):
        tiles.append(tile)

corner_ids = [t.id for t in puzzle.corners()]
print(f'PART ONE: {reduce(lambda x,y: x*y, corner_ids)}')


def find_monsters(image: Image):
    for _ in range(2):
        for _ in Direction:
            if monsters := image.sea_monsters():
                return monsters
            image = image.rotate(1)
        image = image.flip()

image = puzzle.image
sea_monsters = find_monsters(image)
points = set.union(*[x.points for x in sea_monsters])
print(f'PART TWO: {image.count_hash() - len(points)}')
