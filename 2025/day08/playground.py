from __future__ import annotations
import aoc
import itertools
import math
    

JunctionBox = tuple[int, int, int]
Circuit = frozenset[JunctionBox]
    
def distance(x: JunctionBox, y: JunctionBox) -> float:
    dist = (x[0] - y[0], x[1] - y[1], x[2] - y[2])
    return math.hypot(*dist)


@aoc.register(__file__)
def answers():
    data = 'data'
    circuit_count = 10 if data == 'small' else 1000
    boxes: list[JunctionBox] = [tuple(map(int, x.split(','))) for x in aoc.read_lines(data)]
    distances = sorted(itertools.combinations(boxes, 2), key=lambda x: distance(*x))
    circuits = set(frozenset({box}) for box in boxes)

    for i, pair in enumerate(distances, start=1):
        circuit_a, circuit_b = (next(c for c in circuits if x in c) for x in pair)
        circuits -= {circuit_a, circuit_b}
        circuits.add(circuit_a | circuit_b)

        if i == circuit_count:
            sorted_circuits = list(sorted(circuits, key=lambda x: len(x), reverse=True))
            yield math.prod(len(x) for x in sorted_circuits[:3])
        if len(circuits) == 1:
            yield math.prod(x[0] for x in pair)
            break

if __name__ == '__main__':
    aoc.run()
