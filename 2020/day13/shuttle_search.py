from dataclasses import dataclass
import math
from typing import Tuple
import numpy as np


with open('2020/day13/small.txt') as f:
    init_time, schedule = f.read().splitlines()

init_time = int(init_time)
bus_ids = np.array([int(x) for x in schedule.split(',') if x != 'x'])

distances = bus_ids - (init_time % bus_ids)
idx = np.where(distances == min(distances))
nearest_bus = bus_ids[idx][0]
wait_time = distances[idx][0]
print(f'PART ONE: {nearest_bus * wait_time}')


@dataclass
class Cycle:
    cycle_time: int
    offset: int

    def __init__(self, cycle_time: int, offset: int):
        self.cycle_time = cycle_time
        self.offset = offset % cycle_time

    def at(self, t: int) -> int:
        return int(self.cycle_time * t + self.offset)

    def get_off(self):
        return self.offset % self.cycle_time

def euclidian(a: int, b: int, c: int) -> Tuple[int, int]:
    gcd = np.gcd(a,b)
    if c % gcd != 0:
        raise
    k = c/gcd

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

    return s[-2]*k, t[-2]*k

def find_convergence(cycle_a: Cycle, cycle_b: Cycle) -> Cycle:
    a = cycle_a.cycle_time
    b = cycle_b.cycle_time
    c = cycle_b.offset - cycle_a.offset
    s, t = euclidian(a, b, c)

    if not (a*s + b*t == c):
        raise

    offset = abs(cycle_a.at(t=s))
    cycle_time = cycle_a.cycle_time * cycle_b.cycle_time
    return Cycle(cycle_time=cycle_time, offset=offset)


schedule = '17,x,13,19'
cycles = []
for idx, bus in enumerate(schedule.split(',')):
    if (bus == 'x'):
        continue
    cycles.append(Cycle(int(bus), -1*idx))
print(cycles)

main_cycle = cycles[0]
for c in cycles[1:]:
    main_cycle = find_convergence(main_cycle, c)
    print(main_cycle)
print(main_cycle)
