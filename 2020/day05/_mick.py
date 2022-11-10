STARTING_ROWS = [*range(0, 128)]
STARTING_COL = [*range(0, 8)]

with open('2020/day05/data.txt', 'r') as f:
    seats = [s for s in f.read().split()]


def char_select(char: str, section: list):
    front_half = section[:len(section)//2]
    back_half = section[len(section)//2:]

    if char == "B":
        return back_half
    if char == "F":
        return front_half
    if char == "R":
        return back_half
    if char == "L":
        return front_half


def find_section(string: str, section: list, i: int):
    section = char_select(string[i], section)
    if i == len(string) - 1:
        return section
    else:
        i += 1
        return find_section(string, section, i)


def seat_ids():
    new_list = []
    for seat in seats:
        row = find_section(seat[:7], STARTING_ROWS, 0)
        column = find_section(seat[7:], STARTING_COL, 0)
        new_list.append(row[0] * 8 + column[0])
    new_list.sort()
    return new_list


def find_your_seat(ids: list):
    for idx, id in enumerate(ids):
        if id + 1 != ids[idx + 1]:
            return id + 1


print(find_your_seat(seat_ids()))