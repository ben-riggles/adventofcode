import numpy as np
from typing import Tuple


def parse_seat(seat: str) -> Tuple[int, int]:
    row = seat[:-3].replace('F', '0').replace('B', '1')
    col = seat[-3:].replace('L', '0').replace('R', '1')
    return int(row, base=2), int(col, base=2)

def seat_id(row, col) -> int:
    return row * 8 + col


with open('2020/day05/data.txt') as f:
    seats = np.array([parse_seat(line) for line in f.read().splitlines()])

seats = np.column_stack((seats, seat_id(seats[:,0], seats[:,1])))
print(f'PART ONE: {max(seats[:,2])}')


seat_ids = set(seats[:,2])
missing = set(range(max(seats[:,2]))) - seat_ids
missing = [x for x in missing if {x-1, x+2} <= seat_ids]
print(f'PART TWO: {missing[0]}')
