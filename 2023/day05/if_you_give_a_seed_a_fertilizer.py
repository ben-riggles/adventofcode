from __future__ import annotations
import aoc
from aoc.utils import pairwise
from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Generator


@dataclass
class Range:
    start: int
    end: int

    def __contains__(self, val: int | Range) -> bool:
        match val:
            case int(): return self.start <= val <= self.end
            case Range(): return val.end > self.start and val.start < self.end

@dataclass
class MapRule:
    dest: int
    bounds: Range
            
    def apply(self, val: int | Range) -> int:
        match val:
            case int(): return (val - self.bounds.start) + self.dest
            case Range(): return Range(
                start = self.apply(max(val.start, self.bounds.start)),
                end = self.apply(min(val.end, self.bounds.end)),
            )

class AlmanacMap:
    def __init__(self, rules: list[MapRule]):
        self.rules = rules

    def convert(self, val: int | Range) -> Generator[int | Range]:
        for rule in self.rules:
            if val in rule.bounds:
                yield rule.apply(val)
                if type(val) is Range:
                    if val.end not in rule.bounds:
                        yield from self.convert(Range(rule.bounds.end, val.end))
                    if val.start not in rule.bounds:
                        yield from self.convert(Range(val.start, rule.bounds.start))
                return
        yield val
    
    def convert_all(self, values: Iterable[int | Range]) -> Generator[int | Range]:
        for v in values:
            yield from self.convert(v)

    @staticmethod
    def from_string(map_str: str) -> AlmanacMap:
        rules = []
        for rule in map_str.splitlines()[1:]:
            params = tuple(map(int, rule.split()))
            rules.append(MapRule(
                dest = params[0],
                bounds = Range(start = params[1], end = params[1] + params[2] - 1)
            ))
        return AlmanacMap(rules)


@aoc.register(__file__)
def answers():
    data = aoc.read_chunks()
    seeds = list(map(int, data[0].split(':')[1].split()))
    maps = [AlmanacMap.from_string(x) for x in data[1:]]
    
    part_one = reduce(lambda x, y: y.convert_all(x), maps, seeds)
    yield min(part_one)

    part_two = [Range(start=start, end=start+_len-1) for start, _len in pairwise(seeds)]
    part_two = reduce(lambda x, y: y.convert_all(x), maps, part_two)
    yield min([x.start for x in part_two])

if __name__ == '__main__':
    aoc.run()
