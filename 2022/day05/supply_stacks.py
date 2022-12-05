import aoc
from collections import deque
from copy import deepcopy
from functools import reduce
import re


Stacks = dict[int, deque[str]]

def parse_state(state: str) -> Stacks:
    lines = state.splitlines()
    crates, stacks = lines[:-1], lines[-1]
    retval = {}
    for i, stack_no in enumerate(stacks):
        if stack_no == ' ':
            continue
        retval[int(stack_no)] = deque([row[i] for row in reversed(crates) if row[i] != ' '])
    return retval

def move(stacks: Stacks, movement: str, reverse=True) -> Stacks:
    m = re.match(r'move (?P<amount>\d+) from (?P<start>\d+) to (?P<end>\d+)', movement).groupdict()
    to_move = [stacks[int(m['start'])].pop() for _ in range(int(m['amount']))]
    stacks[int(m['end'])].extend(to_move if reverse else reversed(to_move))
    return stacks


@aoc.register(__file__)
def answers():
    initial_state, movements = aoc.read_chunks()
    stacks = parse_state(initial_state)
    
    stacks1 = deepcopy(stacks)
    stacks1 = reduce(lambda x,y: move(x, y), movements.splitlines(), stacks1)
    yield ''.join([q[-1] for q in stacks1.values()])

    stacks2 = deepcopy(stacks)
    stacks2 = reduce(lambda x,y: move(x, y, reverse=False), movements.splitlines(), stacks2)
    yield ''.join([q[-1] for q in stacks2.values()])

if __name__ == '__main__':
    aoc.run()
