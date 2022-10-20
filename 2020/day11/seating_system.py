from enum import Enum, auto
import numpy as np

FLOOR = '.'
EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'


with open('2020/day11/data.txt') as f:
    INITIAL_LAYOUT = np.array([list(line) for line in f.read().splitlines()])


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UPPER_LEFT = auto()
    UPPER_RIGHT = auto()
    LOWER_LEFT = auto()
    LOWER_RIGHT = auto()


def adjacent_seats(layout, direction: Direction):
    match direction:
        case Direction.UP: retval = np.pad(layout, ((0,1), (0,0)))[1:, :]
        case Direction.DOWN: retval = np.pad(layout, ((1,0), (0,0)))[:-1, :]
        case Direction.LEFT: retval = np.pad(layout, ((0,0), (1,0)))[:, :-1]
        case Direction.RIGHT: retval = np.pad(layout, ((0,0), (0,1)))[:, 1:]
        case Direction.UPPER_LEFT: retval = np.pad(layout, ((0,1), (1,0)))[1:, :-1]
        case Direction.UPPER_RIGHT: retval = np.pad(layout, ((0,1), (0,1)))[1:, 1:]
        case Direction.LOWER_LEFT: retval = np.pad(layout, ((1,0), (1,0)))[:-1, :-1]
        case Direction.LOWER_RIGHT: retval = np.pad(layout, ((1,0), (0,1)))[:-1, 1:]
        case _: raise Exception('Invalid direction')
    retval[retval == '0'] = FLOOR
    return retval
    
def count_adjacent_seats(layout, direction: Direction) -> int:
    occ = layout == OCCUPIED_SEAT
    return adjacent_seats(occ, direction=direction)

def occupy_seats(layout, count_method=count_adjacent_seats):
    seats = sum([count_method(layout, d) for d in Direction])

    retval = np.copy(layout)
    retval[(retval == EMPTY_SEAT) & (seats == 0)] = OCCUPIED_SEAT
    return retval

def leave_seats(layout, tolerance, count_method=count_adjacent_seats):
    seats = sum([count_method(layout, d) for d in Direction])

    retval = np.copy(layout)
    retval[(retval == OCCUPIED_SEAT) & (seats >= tolerance)] = EMPTY_SEAT
    return retval
    

layout1 = np.copy(INITIAL_LAYOUT)
while True:
    step_one = occupy_seats(layout1)
    step_two = leave_seats(step_one, tolerance=4)

    if np.array_equal(layout1, step_two):
        break
    layout1 = step_two

occupied_count = np.count_nonzero(layout1 == OCCUPIED_SEAT)
print(f'PART ONE: {occupied_count}')


def sightline(layout, direction: Direction):
    retval = np.copy(layout)
    shifted = adjacent_seats(layout, direction)
    _slice = np.where(retval == FLOOR)
    retval[_slice] = shifted[_slice]

    if not np.array_equal(layout, retval):
        return sightline(retval, direction)
    return retval

def count_seen_seats(layout, direction: Direction) -> int:
    seen_seats = sightline(layout, direction)
    occ = seen_seats == OCCUPIED_SEAT
    return adjacent_seats(occ, direction)


layout2 = np.copy(INITIAL_LAYOUT)
while True:
    step_one = occupy_seats(layout2, count_method=count_seen_seats)
    step_two = leave_seats(step_one, tolerance=5, count_method=count_seen_seats)

    if np.array_equal(layout2, step_two):
        break
    layout2 = step_two

occupied_count = np.count_nonzero(layout2 == OCCUPIED_SEAT)
print(f'PART TWO: {occupied_count}')
