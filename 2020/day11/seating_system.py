import aoc
from enum import Enum, auto
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import convolve
from typing import Callable


FLOOR = 0
EMPTY = 1
OCCUPIED = 2

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UPPER_LEFT = auto()
    UPPER_RIGHT = auto()
    LOWER_LEFT = auto()
    LOWER_RIGHT = auto()


def adjacent_seats(layout: NDArray, direction: Direction) -> NDArray:
    match direction:
        case Direction.UP: retval = np.pad(layout, ((0,1), (0,0)))[1:, :]
        case Direction.DOWN: retval = np.pad(layout, ((1,0), (0,0)))[:-1, :]
        case Direction.LEFT: retval = np.pad(layout, ((0,0), (1,0)))[:, :-1]
        case Direction.RIGHT: retval = np.pad(layout, ((0,0), (0,1)))[:, 1:]
        case Direction.UPPER_LEFT: retval = np.pad(layout, ((0,1), (1,0)))[1:, :-1]
        case Direction.UPPER_RIGHT: retval = np.pad(layout, ((0,1), (0,1)))[1:, 1:]
        case Direction.LOWER_LEFT: retval = np.pad(layout, ((1,0), (1,0)))[:-1, :-1]
        case Direction.LOWER_RIGHT: retval = np.pad(layout, ((1,0), (0,1)))[:-1, 1:]
    return retval

def count_adjacent_seats(layout: NDArray) -> NDArray:
    window = np.array([[1,1,1],[1,0,1],[1,1,1]])
    return convolve(np.where(layout == OCCUPIED, 1, 0), window, mode='constant')

def sightline(layout: NDArray, direction: Direction) -> NDArray:
    retval = np.copy(layout)
    shifted = adjacent_seats(layout, direction)
    _slice = np.where(retval == FLOOR)
    retval[_slice] = shifted[_slice]

    if not (layout == retval).all():
        return sightline(retval, direction)
    return adjacent_seats(retval, direction) == OCCUPIED

def count_seen_seats(layout: NDArray) -> int:
    count = [sightline(layout, d) for d in Direction]
    return sum(count)


def occupy_seats(layout: NDArray, count: NDArray) -> NDArray:
    retval = np.copy(layout)
    retval[(retval == EMPTY) & (count == 0)] = OCCUPIED
    return retval

def leave_seats(layout: NDArray, count: NDArray, tolerance: int) -> NDArray:
    retval = np.copy(layout)
    retval[(retval == OCCUPIED) & (count >= tolerance)] = EMPTY
    return retval

def perform_round(layout: NDArray, tolerance: int, count_method: Callable) -> NDArray:
    count = count_method(layout)
    step_one = occupy_seats(layout, count)
    step_two = leave_seats(step_one, count, tolerance)

    if (layout == step_two).all():
        raise StopIteration
    return step_two


def main():
    transform = str.maketrans('.L#','012')
    initial_layout = np.array([[int(x) for x in list(line.translate(transform))]
                                for line in aoc.read_lines()])

    layout1 = np.copy(initial_layout)
    while True:
        try:
            layout1 = perform_round(layout1, tolerance=4, count_method=count_adjacent_seats)
        except StopIteration:
            break
    part1 = np.count_nonzero(layout1 == OCCUPIED)

    layout2 = np.copy(initial_layout)
    while True:
        try:
            layout2 = perform_round(layout2, tolerance=5, count_method=count_seen_seats)
        except StopIteration:
            break
    part2 = np.count_nonzero(layout2 == OCCUPIED)

    aoc.print_results(part1, part2)

if __name__ == '__main__':
    main()
