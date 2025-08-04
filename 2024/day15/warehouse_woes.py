import aoc
from aoc.grid import KeyGrid, Point, Direction


class WallError(Exception):
    pass


class WarehouseGrid(KeyGrid):
    fields = {
        'robot': '@',
        'boxes': 'O',
        'walls': '#'
    }

    DIR_MAP = {'^': Direction.UP, '>': Direction.RIGHT, 'v': Direction.DOWN, '<': Direction.LEFT}

    @property
    def robot(self) -> Point:
        return next(iter(self.points['robot']))
    
    def process(self, movements) -> set[Point]:
        robot = self.robot
        walls = self['walls']
        boxes = self['boxes']

        for move in movements:
            d = self.DIR_MAP[move]
            next_pos = robot + d.movement

            if next_pos in walls:
                continue
            if next_pos not in boxes:
                robot = next_pos
                continue

            box = next_pos
            while box in boxes:
                box += d.movement
            if box in walls:
                continue
            boxes = (boxes - {next_pos}) | {box}
            robot = next_pos
        return boxes
        
    
class ExpandedWarehouseGrid(WarehouseGrid):
    fields = {
        'robot': '@',
        'boxes_left': '[',
        'boxes_right': ']',
        'walls': '#'
    }

    def process(self, movements) -> set[Point]:
        robot = self.robot
        walls = self['walls']
        boxes_left = self['boxes_left']
        boxes_right = self['boxes_right']

        for move in movements:
            d = self.DIR_MAP[move]
            next_pos = robot + d.movement

            if next_pos in walls:
                continue
            if next_pos not in boxes_left | boxes_right:
                robot = next_pos
                continue

            to_move = {next_pos}
            moved = set()
            if next_pos in boxes_left:
                to_move.add(Point(next_pos.x+1, next_pos.y))
            else:
                to_move.add(Point(next_pos.x-1, next_pos.y))

            try:
                while to_move:
                    if (loc := to_move.pop()) in moved:
                        continue

                    new_loc = loc.move(d)
                    if new_loc in boxes_left:
                        to_move |= {new_loc, new_loc.move(Direction.RIGHT)}
                    elif new_loc in boxes_right:
                        to_move |= {new_loc, new_loc.move(Direction.LEFT)}
                    elif new_loc in walls:
                        raise WallError
                    
                    moved.add(loc)
            except WallError:
                continue

            left_moves = moved & boxes_left
            right_moves = moved & boxes_right
            boxes_left = (boxes_left - left_moves) | {x.move(d) for x in left_moves}
            boxes_right = (boxes_right - right_moves) | {x.move(d) for x in right_moves}
            robot = next_pos

        return boxes_left

    
def gps_coordinate(box: Point) -> int:
    return 100 * box.y + box.x

@aoc.register(__file__)
def answers():
    warehouse, movements = aoc.read_chunks()
    grid = WarehouseGrid(warehouse)
    movements = movements.replace('\n', '')
    
    boxes = grid.process(movements)
    yield sum(gps_coordinate(box) for box in boxes)

    warehouse = warehouse.replace('#', '##').replace('.', '..').replace('O', '[]').replace('@', '@.')
    grid2 = ExpandedWarehouseGrid(warehouse)
    boxes = grid2.process(movements)
    yield sum(gps_coordinate(box) for box in boxes)

if __name__ == '__main__':
    aoc.run()
