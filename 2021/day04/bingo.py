import numpy as np

class Board:
    def __init__(self, values):
        self.values = np.array(values)
        self.marks = np.full((5, 5), fill_value=False, dtype=bool)

    def mark(self, value):
        idx = np.where(self.values == value)
        self.marks[idx] = True

    def bingo(self):
        # Check rows
        for row in self.marks:
            if False not in row:
                return True

        # Check columns
        for col in self.marks.transpose():
            if False not in col:
                return True

    def score(self, last_num):
        idx = np.where(self.marks == False)
        return self.values[idx].sum() * last_num


def main(numbers, boards):
    for num in numbers:
        for board in boards:
            board.mark(num)

        if len(boards) == 1 and boards[0].bingo():
            return boards[0].score(num)
        boards = [x for x in boards if not x.bingo()]
    return 0


_boards = []
with open('day04/bingo_input.txt') as f:
    _numbers = list(map(int, f.readline().strip().split(',')))
    _ = f.readline().strip()

    contents = []
    for line in f:
        line = line.strip()
        if not line:
            _boards.append(Board(values=contents))
            contents = []
            continue

        contents.append(list(map(int, line.split())))



print(main(_numbers, _boards))
