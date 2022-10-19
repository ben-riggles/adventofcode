import numpy as np

FLOOR = '.'
EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'


def count_adjacent_seats(layout):
    occ = layout == OCCUPIED_SEAT
    left, right = np.pad(occ, ((0,0), (1,0)))[:, :-1], np.pad(occ, ((0,0), (0,1)))[:, 1:]
    down, up = np.pad(occ, ((1,0), (0,0)))[:-1, :], np.pad(occ, ((0,1), (0,0)))[1:, :]
    down_left, down_right = np.pad(up, ((0,0), (1,0)))[:, :-1], np.pad(up, ((0,0), (0,1)))[:, 1:]
    up_left, up_right = np.pad(down, ((0,0), (1,0)))[:, :-1], np.pad(down, ((0,0), (0,1)))[:, 1:]
    
    return sum([
        left, right, down, up, down_left, down_right, up_left, up_right
    ])

def occupy_seats(layout, count_method=count_adjacent_seats):
    adjacent = count_method(layout)

    retval = np.copy(layout)
    retval[(retval == EMPTY_SEAT) & (adjacent == 0)] = OCCUPIED_SEAT
    return retval

def leave_seats(layout, tolerance, count_method=count_adjacent_seats):
    adjacent = count_method(layout)

    retval = np.copy(layout)
    retval[(retval == OCCUPIED_SEAT) & (adjacent >= tolerance)] = EMPTY_SEAT
    return retval


with open('2020/day11/small.txt') as f:
    layout = np.array([list(line) for line in f.read().splitlines()])
    

while True:
    step_one = occupy_seats(layout)
    step_two = leave_seats(step_one, tolerance=4)

    if np.array_equal(layout, step_two):
        break
    layout = step_two

occupied_count = np.count_nonzero(layout == OCCUPIED_SEAT)
print(layout)
print(f'PART ONE: {occupied_count}')


def count_seen_seats(layout):
    pass

# while True:
#     step_one = occupy_seats(layout, count_method=count_seen_seats)
#     step_two = leave_seats(step_one, tolerance=5, count_method=count_seen_seats)

#     if np.array_equal(layout, step_two):
#         break
#     layout = step_two

# occupied_count = np.count_nonzero(layout == OCCUPIED_SEAT)
# print(layout)
# print(f'PART TWO: {occupied_count}')