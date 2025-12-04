from abc import ABC, abstractmethod
import aoc
from aoc.grid import Point
from dataclasses import dataclass, field
import functools
from typing import ClassVar


@dataclass
class Keypad(ABC):
    position: Point = field(init=False, default=None)
    keymap: ClassVar[dict[str, Point]]

    def __post_init__(self):
        self.reset()

    @staticmethod
    def _path_base(up_down: str, left_right: str) -> str:
        if '^' in up_down and '<' in left_right: return left_right + up_down
        if 'v' in up_down and '<' in left_right: return left_right + up_down
        if 'v' in up_down and '>' in left_right: return up_down + left_right
        if '^' in up_down and '>' in left_right: return up_down + left_right
        return up_down + left_right

    @abstractmethod
    @classmethod
    @functools.cache
    def path(cls, start: Point, end: Point) -> str:
        pass
    
    @abstractmethod
    @functools.cache
    def press(self, button: str) -> int:
        pass

    def reset(self):
        self.position = self.keymap['A']

class NumericKeypad(Keypad):
    keymap = {
        '7': Point(0, 0), '8': Point(1, 0), '9': Point(2, 0),
        '4': Point(0, 1), '5': Point(1, 1), '6': Point(2, 1),
        '1': Point(0, 2), '2': Point(1, 2), '3': Point(2, 2),
        ' ': Point(0, 3), '0': Point(1, 3), 'A': Point(2, 3),
    }

    @classmethod
    @functools.cache
    def path(cls, start: Point, end: Point) -> str:
        x_diff = end.x - start.x
        y_diff = end.y - start.y
        up_down = ('v' if y_diff > 0 else '^') * abs(y_diff)
        left_right = ('>' if x_diff > 0 else '<') * abs(x_diff)
        
        if start.y == 3 and end.x == 0:
            return up_down + left_right + 'A'
        elif start.x == 0 and end.y == 3: 
            return left_right + up_down + 'A'
        return cls._path_base(up_down, left_right) + 'A'

    @functools.cache
    def press(self, button: str) -> int:
        new_loc = self.keymap[button]
        path = NumericKeypad.path(self.position, new_loc)
        return len(path)

@dataclass
class DirectionalKeypad(Keypad):
    child: Keypad
    keymap = {
        ' ': Point(0, 0), '^': Point(1, 0), 'A': Point(2, 0),
        '<': Point(0, 1), 'v': Point(1, 1), '>': Point(2, 1),
    }

    @classmethod
    @functools.cache
    def path(cls, start: Point, end: Point) -> str:
        x_diff = end.x - start.x
        y_diff = end.y - start.y
        up_down = ('v' if y_diff > 0 else '^') * abs(y_diff)
        left_right = ('>' if x_diff > 0 else '<') * abs(x_diff)
        
        if start.x == 0:
            return left_right + up_down + 'A'
        elif end.x == 0:
            return up_down + left_right + 'A'
        return cls._path_base(up_down, left_right) + 'A'

    def press(self, button: str) -> str:
        if isinstance(self.child, NumericKeypad):
            return self.child.press(button)
        
        child_sequence = self.path(button)
        child_sequence = self.child.press(button)
        presses = 0

        for move in child_sequence:
            presses += self.child

        return sequence
    
    def complexity(self, code: str) -> int:
        sequence = ''
        for button in code:
            sequence += self.press(button)
        self.reset()

        numeric = int(''.join(x for x in code if x.isdigit()))
        return len(sequence) * numeric


@aoc.register(__file__)
def answers():
    codes = aoc.read_lines()
    keypads = [NumericKeypad()]
    for x in range(26):
        keypads.append(DirectionalKeypad(child=keypads[x-1]))

    complexities = [keypads[-1].complexity(x) for x in codes]
    yield sum(complexities)

if __name__ == '__main__':
    aoc.run()
