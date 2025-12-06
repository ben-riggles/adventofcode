import aoc
from itertools import groupby, zip_longest
import math
from typing import Callable, Iterable


def operator(op_str: str) -> Callable[[Iterable[int]], int]:
    match op_str:
        case '+': return sum
        case '*': return math.prod

def solve_1(problem: list[str]) -> int:
    problem = [''.join(x).strip() for x in zip(*problem)]
    op = operator(problem[-1])
    return op(map(int, problem[:-1]))

def solve_2(problem: list[str]) -> int:
    op = operator(''.join([x[-1] for x in problem]).strip())
    vals = [int(x[:-1]) for x in problem]
    return op(vals)


@aoc.register(__file__)
def answers():
    problems = [''.join(x) for x in (zip_longest(*aoc.read_lines(), fillvalue=' '))]
    problems = [list(g) for k, g in groupby(problems, lambda x: x.strip() != '') if k]
    yield sum(solve_1(x) for x in problems)
    yield sum(solve_2(x) for x in problems)

if __name__ == '__main__':
    aoc.run()
