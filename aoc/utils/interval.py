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
            case Interval(): return self.start <= val.end and self.end >= val.start

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
        return self.end - self.start + 1
    
    def __and__(self, val: int | Interval) -> int | Interval:
        match val:
            case int(): return val if val in self else 0
            case Interval(): return self.intersection(val)
    
    def __iter__(self):
        return iter(range(self.start, self.end))
    
    def intersection(self, other: Interval) -> Interval:
        if self not in other:
            return None
        return Interval(
            start = max(self.start, other.start),
            end = min(self.end, other.end),
        )
    
    def difference(self, other: Interval) -> list[Interval]:
        retval = []
        if self < other or self not in other:
            return []
        if self.start not in other:
            retval.append(Interval(self.start, other.start - 1))
        if self.end not in other:
            retval.append(Interval(other.end + 1, self.end))
        return retval
    
    def union(self, other: Interval) -> Interval:
        if self not in other:
            return None
        return Interval(
            start = min(self.start, other.start),
            end = max(self.end, other.end)
        )
