import aoc
import itertools
from operator import add, mul


def run(intcode: list[int], noun: int = 0, verb: int = 0) -> int:
    _intcode = intcode[:]
    _intcode[1] = noun
    _intcode[2] = verb

    pointer = 0
    while _intcode[pointer] != 99:
        match _intcode[pointer]:
            case 1: op = add
            case 2: op = mul
            case _: raise Exception("Invalid opcode detected")
            
        _intcode[pointer+3] = op(_intcode[pointer+1], _intcode[pointer+2])
        pointer += 4
    return _intcode[0]

def detect(intcode: list[int], target: int) -> int:
    for n, v in itertools.product(range(100), range(100)):
        if run(intcode, n, v) == target:
            return 100 * n + v

@aoc.register(__file__)
def answers():
    intcode = list(map(int, aoc.read_data().split(',')))
    yield run(intcode, noun=12, verb=2)
    yield detect(intcode, target=19690720)

if __name__ == '__main__':
    aoc.run()
