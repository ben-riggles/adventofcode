import numpy as np
from collections import deque

with open('day10/navigation_subsystem.txt') as f:
    signals = f.read().splitlines()

class CorruptionError(ValueError):
    score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    def __init__(self, corruption):
        super().__init__('Corruption occurred')
        self.corruption = corruption
        self.score = CorruptionError.score[corruption]


class Sequence:
    openers = ['(', '[', '{', '<']
    close_map = {'(': ')', '[': ']', '{': '}', '<': '>'}

    def __init__(self, chunk):
        self.sequences = []
        self.opener = self.closer = None

        while (chunk):
            next_char = chunk[0]
            if not self.opener:
                self.opener = chunk.popleft()
            elif self.can_close(next_char):
                self.closer = chunk.popleft()
                break
            elif next_char in Sequence.openers:
                self.sequences.append(Sequence(chunk))
            else:
                raise CorruptionError(chunk.popleft())

    def __str__(self):
        inner = ''.join([str(x) for x in self.sequences])
        closer = self.closer if self.closer is not None else ''
        return f'{self.opener}{inner}{closer}'

    def can_close(self, c):
        try:
            return Sequence.close_map[self.opener] == c
        except KeyError:
            raise CorruptionError(self.opener)

    def closed(self):
        return self.closer is not None and all([x.closed() for x in self.sequences])

    def close(self):
        if self.closed():
            return []
        if not self.sequences:
            return [Sequence.close_map[self.opener]]
        return self.sequences[-1].close() + [Sequence.close_map[self.opener]]


class Chunk:
    def __init__(self, chunk_str):
        self.sequences = []
        self.corruption = None
        chunk_q = deque(list(chunk_str))

        while (chunk_q):
            try:
                self.sequences.append(Sequence(chunk_q))
            except CorruptionError as e:
                self.corruption = e
                break

    def __str__(self):
        if self.corruption:
            return f'CORRUPTED: {self.corruption.corruption}'
        else:
            return ''.join([str(x) for x in self.sequences])

    def close(self):
        if self.corruption is not None:
            return []
        return self.sequences[-1].close()


# Part 1
print('---------- Part 1 ----------')

chunks = [Chunk(x) for x in signals]
[print(x) for x in chunks]
score = sum([x.corruption.score for x in chunks if x.corruption is not None])
print(f'{score=}')


# Part 2
print('\n\n---------- Part 2 ----------')

def calculate_score(closer):
    score_chart = {')': 1, ']': 2, '}': 3, '>': 4}
    score = 0
    for c in closer:
        score *= 5
        score += score_chart[c]
    return score

closers = [x.close() for x in chunks]
closers = [x for x in closers if x]
[print(x) for x in closers]

scores = [calculate_score(x) for x in closers]
print(scores)
print(int(np.median(scores)))
