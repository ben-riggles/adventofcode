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


missing = []
for row in np.unique(seats[:,0]):
    row_seats = seats[seats[:,0] == row]
    open_seats = set(range(0, 8)) - set(row_seats[:,1])
    missing.extend([(row, x, seat_id(row, x)) for x in open_seats])

missing = [x for x in missing if x[2]+1 in seats[:,2] and x[2]-1 in seats[:,2]]
print(f'PART TWO: {missing[0][2]}')
