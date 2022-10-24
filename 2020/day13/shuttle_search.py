from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
import math
import numpy as np
from operator import iand
from typing import Tuple


with open('2020/day13/data.txt') as f:
    init_time, schedule = f.read().splitlines()

init_time = int(init_time)
bus_ids = np.array([int(x) for x in schedule.split(',') if x != 'x'])

distances = bus_ids - (init_time % bus_ids)
idx = np.where(distances == min(distances))
nearest_bus = bus_ids[idx][0]
wait_time = distances[idx][0]
print(f'PART ONE: {nearest_bus * wait_time}')


def euclidean(a: int, b: int, c: int) -> Tuple[int, int]:
    gcd = math.gcd(a, b)
    k = int(c/gcd)

    q = [0,0]
    r = [a,b]
    s = [1,0]
    t = [0,1]
    
    while r[-1] != 0:
        quotient = r[-2] / r[-1]
        q.append(math.floor(quotient) if quotient >=0 else math.ceil(quotient))
        r.append(r[-2] - q[-1] * r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])

    s, t = s[-2], t[-2]
    if a*s + b*t == -gcd:
        k = -k
    return s*k, t*k

@dataclass
class Cycle:
    cycle_time: int
    offset: int

    def __init__(self, cycle_time: int, offset: int):
        self.cycle_time = cycle_time
        self.offset = offset % cycle_time

    def at(self, t: int) -> int:
        return int(self.cycle_time * t + self.offset)

    def __and__(self, other: Cycle) -> Cycle:
        s, _ = euclidean(self.cycle_time, -other.cycle_time, other.offset - self.offset)
        return Cycle(
            cycle_time=math.lcm(self.cycle_time, other.cycle_time),
            offset=self.at(s)
        )


cycles = [Cycle(int(bus), -1*idx) for idx, bus in enumerate(schedule.split(',')) if bus != 'x']
main_cycle: Cycle = reduce(iand, cycles)
print(f'PART TWO: {main_cycle.offset}')
