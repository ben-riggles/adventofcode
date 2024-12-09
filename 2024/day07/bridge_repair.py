import aoc
from collections import deque


def parse_equation(line: str) -> tuple[int, tuple[int]]:
    test_value, operators = line.split(':')
    return int(test_value), tuple(map(int, operators.split()))

def try_equation(ops: list[str], test_value: int, numbers: tuple[int]) -> int:
    state = (test_value, numbers)
    queue = deque([state])

    while queue:
        value, numbers = queue.pop()
        
        if len(numbers) == 0:
            if (value == 0):
                return test_value
            continue

        if '+' in ops and value >= numbers[-1]:
            queue.append((value - numbers[-1], numbers[:-1]))
        if '*' in ops and value % numbers[-1] == 0:
            queue.append((value // numbers[-1], numbers[:-1]))

        str_val = str(value)
        str_num = str(numbers[-1])
        if '||' in ops and str_val.endswith(str_num):
            new_val = 0 if value == numbers[-1] else int(str_val[:-len(str_num)])
            queue.append((int(new_val), numbers[:-1]))
    
    return 0


@aoc.register(__file__)
def answers():
    equations = [parse_equation(x) for x in aoc.read_lines()]

    # Part One
    ops = ('+', '*')
    yield sum(try_equation(ops, *x) for x in equations)

    # Part Two
    ops += ('||',)
    yield sum(try_equation(ops, *x) for x in equations)

if __name__ == '__main__':
    aoc.run()
