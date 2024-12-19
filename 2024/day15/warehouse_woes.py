import aoc
from aoc.grid import KeyGrid, Point, Direction


class WarehouseGrid(KeyGrid):
    fields = {
        'robot': '@',
        'boxes': 'O',
        'walls': '#'
    }

    @property
    def robot(self) -> Point:
        return next(iter(self.points['robot']))
    
    def process(self, movements) -> set[Point]:
        dir_map = {'^': Direction.UP, '>': Direction.RIGHT, 'v': Direction.DOWN, '<': Direction.LEFT}
        robot = self.robot
        walls = self['walls']
        boxes = self['boxes']

        for move in movements:
            d = dir_map[move]
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
    
def gps_coordinate(box: Point) -> int:
    return 100 * box.y + box.x

@aoc.register(__file__)
def answers():
    warehouse, movements = aoc.read_chunks()
    warehouse = WarehouseGrid(warehouse)
    movements = movements.replace('\n', '')
    
    boxes = warehouse.process(movements)
    yield sum(gps_coordinate(box) for box in boxes)

if __name__ == '__main__':
    aoc.run()
