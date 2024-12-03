import aoc
import itertools
from operator import add, mul


def run(intcode: list[int], input: int = 1) -> int:
    _intcode = intcode[:]

    pointer = 0
    outputs = []

    def _param(id: int, mode: int):
        match mode:
            case 0: return _intcode[_intcode[pointer+id]]
            case 1: return _intcode[pointer+id]
            case _: raise Exception("Invalid mode detected")

    while _intcode[pointer] != 99:
        instruction = str(_intcode[pointer]).zfill(5)
        opcode = int(instruction[3:])
        args = tuple(map(int, reversed(instruction[:3])))
        
        match opcode:
            case 1 | 2:
                op = add if opcode == 1 else mul
                left = _intcode[_intcode[pointer+1]] if args[0] == 0 else _intcode[pointer+1]
                right = _intcode[_intcode[pointer+2]] if args[1] == 0 else _intcode[pointer+2]

                if args[2] == 0:
                    _intcode[_intcode[pointer+3]] = op(left, right)
                else:
                    _intcode[pointer+3] = op(left, right)
                
                pointer += 4
            case 3:
                arg = _intcode[_intcode[pointer+1]] if args[0] == 0 else _intcode[pointer+1]
                _intcode[arg] = input
                pointer += 2
            case 4:
                arg = _intcode[_intcode[pointer+1]] if args[0] == 0 else _intcode[pointer+1]
                outputs.append(arg)
                pointer += 2
            case _:
                raise Exception("Invalid opcode detected")
    print(outputs)
    return _intcode[0]

@aoc.register(__file__)
def answers():
    intcode = list(map(int, aoc.read_data().split(',')))
    yield run(intcode, input=1)

if __name__ == '__main__':
    aoc.run()
