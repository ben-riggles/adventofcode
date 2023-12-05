from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Interval:
    start: int
    end: int

    def __add__(self, val: int) -> Interval:
        return Interval(start=self.start + val, end=self.end + val)
    
    def __sub__(self, val: int) -> Interval:
        return Interval(start=self.start - val, end=self.end - val)
    
    def __contains__(self, val: int | Interval) -> bool:
        match val:
            case int(): return self.start <= val <= self.end
            case Interval(): return val.end > self.start and val.start < self.end

    def __eq__(self, other: Interval) -> bool:
        return self.start == other.start and self.end == other.end
    
    def __lt__(self, val: int | Interval) -> bool:
        match val:
            case int(): return self.end < val
            case Interval(): return self.start >= val.start and self.end <= val.end

    def __rt__(self, val: int | Interval) -> bool:
        match val:
            case int(): return self.start > val
            case Interval(): return self.start <= val.start and self.end >= val.end

    def __len__(self):
        return self.end - self.start
    
    def __and__(self, other: Interval) -> Interval:
        if not self in other:
            return None
        return Interval(
            start = max(self.start, other.start),
            end = min(self.end, other.end),
        )
    
    def __iter__(self):
        return iter(range(self.start, self.end))


    

    

if __name__ == '__main__':
    i1 = Interval(3, 7)
    i2 = Interval(4, 5)
    i3 = Interval(1, 5)
    i4 = Interval(6, 10)

    print(i1)

    print(i2 & i3)
    print(i3 & i4)
    print(i2+1 & i4)