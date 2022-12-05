import aoc
import re


def parse_line(line: str) -> tuple[set,set]:
    return tuple(map(int, re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line).groups()))

def contains(min_a: int, max_a: int, min_b: int, max_b: int) -> bool:
    return min_a <= min_b and max_a >= max_b or min_b <= min_a and max_b >= max_a

def overlap(min_a: int, max_a: int, min_b: int, max_b: int) -> bool:
    return not (max_a < min_b or max_b < min_a)


@aoc.register(__file__)
def answers():
    assignments = [parse_line(x) for x in aoc.read_lines()]
    yield len([x for x in assignments if contains(*x)])
    yield len([x for x in assignments if overlap(*x)])

if __name__ == '__main__':
    aoc.run()
